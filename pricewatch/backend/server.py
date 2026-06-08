"""
PriceWatch - Backend API Server
Musical Presentes - musicalpresentesonline.com.br
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json, os, threading, time
from datetime import datetime
from scraper import CompetitorScraper
from loja_integrada import LojaIntegradaAPI
from telegram_alerter import TelegramAlerter
from analyzer import PriceAnalyzer

app = Flask(__name__)
CORS(app)

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')
DATA_PATH   = os.path.join(os.path.dirname(__file__), '..', 'data')

def load_config():
    with open(CONFIG_PATH, encoding='utf-8') as f:
        return json.load(f)

def save_data(filename, data):
    os.makedirs(DATA_PATH, exist_ok=True)
    with open(os.path.join(DATA_PATH, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_data(filename):
    path = os.path.join(DATA_PATH, filename)
    if not os.path.exists(path):
        return {}
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def run_scrape_and_alert():
    """Executa scraping + analise + alertas em background"""
    try:
        cfg     = load_config()
        scraper = CompetitorScraper(cfg['competitors'])
        results = scraper.scrape_all()
        save_data('competitors.json', results)

        products = load_data('products.json')
        if not products:
            print("[scheduler] Nenhum produto carregado — execute /api/products primeiro")
            return 0

        analyzer = PriceAnalyzer()
        alerts   = analyzer.generate_alerts(products, results, cfg['alert_thresholds'])
        save_data('alerts.json', alerts)

        if alerts and cfg['telegram']['enabled']:
            tg = TelegramAlerter(cfg['telegram'])
            sent = tg.send_alerts(alerts)
            print(f"[scheduler] {len(alerts)} alertas gerados, {sent} enviados no Telegram")

            # Relatorio diario as 9h
            if datetime.now().hour == 9:
                comparison = analyzer.compare(products, results)
                tg.send_daily_report(comparison)
        else:
            print(f"[scheduler] Scraping OK — {len(results)} lojas, {len(alerts)} alertas")

        return len(alerts)
    except Exception as e:
        print(f"[scheduler] Erro: {e}")
        import traceback; traceback.print_exc()
        return 0

@app.route('/api/status')
def status():
    products = load_data('products.json')
    competitors = load_data('competitors.json')
    alerts = load_data('alerts.json') or []
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'products_loaded': len(products) if isinstance(products, list) else 0,
        'competitors_scraped': len(competitors),
        'alerts': len(alerts),
    })

@app.route('/api/products')
def get_products():
    cfg = load_config()
    if not cfg['loja_integrada'].get('chave_aplicacao') or \
       cfg['loja_integrada']['chave_aplicacao'] == 'COLE_AQUI_QUANDO_CHEGAR_O_EMAIL':
        return jsonify({'error': 'Chave de aplicacao nao configurada'}), 400
    api = LojaIntegradaAPI(
        cfg['loja_integrada']['chave_api'],
        cfg['loja_integrada']['chave_aplicacao']
    )
    products = api.get_products()
    save_data('products.json', products)
    return jsonify({'loaded': len(products), 'products': products[:5]})

@app.route('/api/competitors')
def get_competitors():
    return jsonify(load_data('competitors.json'))

@app.route('/api/comparison')
def get_comparison():
    products    = load_data('products.json')
    competitors = load_data('competitors.json')
    if not products or not competitors:
        return jsonify([])
    analyzer = PriceAnalyzer()
    result   = analyzer.compare(products, competitors)
    return jsonify(result)

@app.route('/api/alerts')
def get_alerts():
    return jsonify(load_data('alerts.json') or [])

@app.route('/api/scrape', methods=['POST'])
def trigger_scrape():
    """Dispara scraping em background e retorna imediatamente"""
    def run():
        run_scrape_and_alert()
    t = threading.Thread(target=run, daemon=True)
    t.start()
    return jsonify({
        'status': 'iniciado',
        'message': 'Scraping iniciado em background. Aguarde ~2 minutos e consulte /api/alerts',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/scrape/sync', methods=['POST'])
def trigger_scrape_sync():
    """Dispara scraping sincronamente e aguarda resultado"""
    n = run_scrape_and_alert()
    alerts = load_data('alerts.json') or []
    return jsonify({'scraped': 7, 'alerts': n, 'timestamp': datetime.now().isoformat()})

@app.route('/api/telegram/test', methods=['POST'])
def test_telegram():
    cfg = load_config()
    tg  = TelegramAlerter(cfg['telegram'])
    tg.enabled = True
    ok = tg.broadcast(
        "✅ PriceWatch funcionando!\n"
        "Musical Presentes · Ipatinga, MG\n\n"
        "Sistema de alertas ativo."
    )
    return jsonify({'sent': ok > 0})

@app.route('/api/update-price', methods=['POST'])
def update_price():
    body = request.json
    cfg  = load_config()
    api  = LojaIntegradaAPI(
        cfg['loja_integrada']['chave_api'],
        cfg['loja_integrada']['chave_aplicacao']
    )
    result = api.update_price(body['product_id'], body['new_price'])
    return jsonify(result)

def scheduler():
    """Roda scraping a cada 6 horas"""
    time.sleep(30)  # aguarda 30s antes do primeiro ciclo
    while True:
        print(f"[{datetime.now()}] Iniciando varredura automatica...")
        run_scrape_and_alert()
        time.sleep(6 * 3600)

if __name__ == '__main__':
    t = threading.Thread(target=scheduler, daemon=True)
    t.start()
    print("PriceWatch iniciado — http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
