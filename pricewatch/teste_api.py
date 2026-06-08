"""
teste_api.py — Rode este script no seu computador para testar a conexão
e me cole o resultado aqui no chat.

Uso:
    python teste_api.py
"""

import requests, json

CHAVE_API        = "a11542bc1dda66018ff6"
CHAVE_APLICACAO  = "3ea077f3-97f3-417f-80cd-326ceaad6519"
BASE_URL         = "https://api.awsli.com.br/v1"

print("=" * 55)
print("  PriceWatch — Teste de Conexão Loja Integrada")
print("=" * 55)

def test(endpoint, label):
    url = f"{BASE_URL}/{endpoint}/"
    try:
        r = requests.get(url, params={
            "chave_api": CHAVE_API,
            "chave_aplicacao": CHAVE_APLICACAO,
            "limit": 10
        }, timeout=15)
        print(f"\n[{label}] Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(json.dumps(data, ensure_ascii=False, indent=2)[:2000])
        else:
            print("Resposta:", r.text[:500])
        return r.status_code == 200
    except Exception as e:
        print(f"[{label}] ERRO: {e}")
        return False

ok = test("produto", "Produtos")
if ok:
    test("categoria", "Categorias")
    print("\n✅ API conectada com sucesso! Cole o resultado acima no chat.")
else:
    print("\n❌ Falha na conexão. Cole o resultado acima no chat.")
