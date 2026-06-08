r = requests.get('https://api.awsli.com.br/v1/produto/', params={'chave_api':'a11542bc1dda66018ff6','chave_aplicacao':'3ea077f3-97f3-417f-80cd-326ceaad6519','limit':50}) 
data = r.json() 
print('Total:', data.get('meta',{}).get('total_count','?')) 
