import requests, json, time

CHAVE_API = "a11542bc1dda66018ff6"
CHAVE_APP = "3ea077f3-97f3-417f-80cd-326ceaad6519"

with open("produtos_completos.json", encoding="utf-8") as f:
    produtos = json.load(f)

print(f"Total: {len(produtos)} produtos. Buscando precos...")
atualizados = []

for i, p in enumerate(produtos):
    pid = p["id"]
    preco = None
    for tentativa in range(3):
        try:
            r = requests.get(
                f"https://api.awsli.com.br/v1/produto/{pid}/",
                params={"chave_api": CHAVE_API, "chave_aplicacao": CHAVE_APP},
                timeout=15
            )
            if r.status_code == 200:
                d = r.json()
                preco = d.get("preco_promocional") or d.get("preco_cheio")
                break
        except:
            time.sleep(2)

    p["preco"] = preco
    atualizados.append(p)

    if preco:
        print(f"[{i+1}/{len(produtos)}] R$ {preco:.2f} | {p['nome'][:50]}")
    else:
        print(f"[{i+1}/{len(produtos)}] sem preco | {p['nome'][:50]}")

    # Salva a cada 50 produtos
    if (i + 1) % 50 == 0:
        with open("produtos_com_preco.json", "w", encoding="utf-8") as f:
            json.dump(atualizados, f, ensure_ascii=False, indent=2)
        print(f">>> Checkpoint salvo: {i+1} produtos")

    time.sleep(0.4)

with open("produtos_com_preco.json", "w", encoding="utf-8") as f:
    json.dump(atualizados, f, ensure_ascii=False, indent=2)

com_preco = [p for p in atualizados if p["preco"]]
print(f"\nConcluido! {len(com_preco)} produtos com preco de {len(atualizados)} total.")
print("Arquivo: produtos_com_preco.json")