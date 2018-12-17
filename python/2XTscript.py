import requests
import json
from itertools import islice
from math import radians, cos, sin, asin, sqrt

apiKey = "phnvlDweeuDLvjSqCqre9mOzvKKdzMmw"

# Pega a lista de aeroportos
airport_list_response = requests.get('http://stub.2xt.com.br/air/airports/phnvlDweeuDLvjSqCqre9mOzvKKdzMmw', auth=('helcio', 'sejvlD'))
airport_list = json.loads(airport_list_response.text)

# Separa a lista em 2 listas de 20 aeroportos
airport_embark = dict(islice(airport_list.items(), 0, 20))
airport_disembark = dict(islice(airport_list.items(), 40, 60))

print(len(airport_embark))
print(len(airport_disembark))

# Teste, deletar depois
# for airport in airport_list:
#    print("{} Latitude: {} Longitute: {}".format(airport, airport_list[airport]["lat"], airport_list[airport]["lon"]))

# date = input("Date (yyyy-mm-dd): ")
date = "2019-01-01"
embark = input("embark iata: ").upper()
disembark = input("disembark iata: ").upper()

url = "http://stub.2xt.com.br/air/search/{}/{}/{}/{}".format(apiKey, embark, disembark, date)

search_reponse = requests.get(url, auth = ('helcio', 'sejvlD'))

# haversine function roubada daqui https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points sorry, mas tenho pouco tempo :)
def haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

lat1 = 0
lat2 = 0
lon1 = 0
lon2 = 0

for a in airport_list:
    if embark == a:
        lat1 = airport_list[a]["lat"]
        lon1 = airport_list[a]["lon"]
    if disembark == a:
        lat2 = airport_list[a]["lat"]
        lon2 = airport_list[a]["lon"]

linear_distance = haversine(lat1, lon1, lat2, lon2)

print("Distancia linear: {}".format(linear_distance))
