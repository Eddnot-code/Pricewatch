import requests, json, time

CHAVE_API = "a11542bc1dda66018ff6"
CHAVE_APP = "3ea077f3-97f3-417f-80cd-326ceaad6519"

todos = []
offset = 0
print("Buscando produtos em lotes...")

while True:
    r = requests.get(
        "https://api.awsli.com.br/v1/produto/",
        params={
            "chave_api": CHAVE_API,
            "chave_aplicacao": CHAVE_APP,
            "limit": 50,
            "offset": offset
        },
        timeout=30
    )
    d = r.json()
    objetos = d.get("objects", [])
    if not objetos:
        break

    for p in objetos:
        if not p or not p.get("nome"):
            continue
        preco = p.get("preco_promocional") or p.get("preco_cheio") or p.get("preco")
        todos.append({
            "id": p.get("id"),
            "nome": p.get("nome", ""),
            "sku": p.get("sku", ""),
            "preco": preco,
            "url": p.get("url", ""),
            "ativo": p.get("ativo", True)
        })
        print(f"{p.get('id')} | {str(p.get('nome',''))[:50]} | R$ {preco}")

    offset += 50
    print(f"--- {len(todos)} produtos carregados ---")
    if not d.get("meta", {}).get("next"):
        break
    time.sleep(0.5)

with open("produtos_completos.json", "w", encoding="utf-8") as f:
    json.dump(todos, f, ensure_ascii=False, indent=2)

print(f"\nConcluido! {len(todos)} produtos salvos em produtos_completos.json")