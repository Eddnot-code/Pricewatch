import requests, json

# Tenta endpoint de preço por produto específico
produto_id = "401155933"
endpoints = [
    f"https://api.awsli.com.br/v1/produto/{produto_id}/",
    f"https://api.awsli.com.br/v1/precificacao/",
    f"https://api.awsli.com.br/v1/produto/?limit=1&id={produto_id}",
]

params = {
    "chave_api": "a11542bc1dda66018ff6",
    "chave_aplicacao": "3ea077f3-97f3-417f-80cd-326ceaad6519"
}

for url in endpoints:
    r = requests.get(url, params=params)
    print(f"\n--- {url} ---")
    print("Status:", r.status_code)
    # Procura qualquer campo com preco no JSON
    try:
        d = r.json()
        txt = json.dumps(d)
        import re
        precos = re.findall(r'"[^"]*prec[^"]*":\s*[^,}\]]+', txt, re.IGNORECASE)
        print("Campos de preco encontrados:", precos[:10])
    except:
        print(r.text[:200])