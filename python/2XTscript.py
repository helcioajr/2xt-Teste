import requests
import json

apiKey = "phnvlDweeuDLvjSqCqre9mOzvKKdzMmw"

r = requests.get('http://stub.2xt.com.br/air/airports/phnvlDweeuDLvjSqCqre9mOzvKKdzMmw', auth=('helcio', 'sejvlD'))

airport_list = json.loads(r.text)

for airport in airport_list:
    print(airport.get("iata"))
