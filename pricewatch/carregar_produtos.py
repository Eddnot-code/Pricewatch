import json, os

with open("produtos_com_preco.json", encoding="utf-8") as f:
    produtos = json.load(f)

com_preco = [p for p in produtos if p.get("preco") and p["preco"] > 10]

os.makedirs("data", exist_ok=True)
with open("data/products.json", "w", encoding="utf-8") as f:
    json.dump(com_preco, f, ensure_ascii=False, indent=2)

print(f"Carregados {len(com_preco)} produtos com preco em data/products.json")