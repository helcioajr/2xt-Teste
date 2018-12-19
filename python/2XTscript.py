import requests
from datetime import datetime, timedelta
import json
from itertools import islice
from math import radians, cos, sin, asin, sqrt

apiKey = "phnvlDweeuDLvjSqCqre9mOzvKKdzMmw"

# Pega a lista de aeroportos
airport_list_response = requests.get('http://stub.2xt.com.br/air/airports/phnvlDweeuDLvjSqCqre9mOzvKKdzMmw', auth=('helcio', 'sejvlD'))
airport_list = json.loads(airport_list_response.text)

# Separa a lista em 2 listas de 20 aeroportos
airport_list1 = dict(islice(airport_list.items(), 0, 20))
airport_list2 = dict(islice(airport_list.items(), 40, 60))


# Definicao da data
date = datetime.now() + timedelta(days=40)
date = date.date()

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

# Retorna a distancia linear
def getLinearDistance(iata1, iata2, airport_list):

    lat1 = 0
    lat2 = 0
    lon1 = 0
    lon2 = 0

    for a in airport_list:
        if iata1 == a:
            lat1 = airport_list[a]["lat"]
            lon1 = airport_list[a]["lon"]
        if iata2 == a:
            lat2 = airport_list[a]["lat"]
            lon2 = airport_list[a]["lon"]

    linear_distance = haversine(lat1, lon1, lat2, lon2)
    return linear_distance

# Classe com os dados dos voos
class Flight:
    departure_time = ""
    arrival_time = ""
    aircraft= ""
    aircraftManufacturer= ""
    avgSpeed=0.0
    farePerKM=0.0

flight_data_List = []

# Calcula a velocidade aproximada
def getAvgSpeed(linear_distance, time_diff):
    (h, m, s) = str(time_diff).split(':')
    t = float(h) + float(m)/60 + float(s)/3600
    avgSpeed = float(linear_distance) / t
    return format(avgSpeed, '.2f')

# Retorna a distancia, velocidade aproximada e valor por km
def getFlightData(linear_distance, flight_list):
    l = []
    for flight in flight_list["options"]:
        f = Flight()
        arrival_time = datetime.strptime(flight["arrival_time"], "%Y-%m-%dT%H:%M:%S")
        departure_time = datetime.strptime(flight["departure_time"], "%Y-%m-%dT%H:%M:%S")
        time_diff = abs(departure_time - arrival_time)
        f.arrival_time = arrival_time
        f.departure_time = departure_time
        f.avgSpeed = getAvgSpeed(linear_distance, time_diff)
        f.farePerKM = format(float(linear_distance) / float(flight["fare_price"]), '.2f')
        f.aircraft = flight["aircraft"]["model"]
        f.aircraftManufacturer = flight["aircraft"]["manufacturer"]

        l.append(f)

    return l

for a1 in airport_list1:
    for a2 in airport_list2:

        iata1 = a1
        iata2 = a2

        url = "http://stub.2xt.com.br/air/search/{}/{}/{}/{}".format(apiKey, iata1, iata2, date)

        # Busca a lista de opçoes de voo
        flight_search_response = requests.get(url, auth = ('helcio', 'sejvlD'))
        flight_list = json.loads(flight_search_response.text)

        linear_distance = getLinearDistance(iata1, iata2, airport_list)
        flight_data_List = getFlightData(linear_distance, flight_list)

        for f in flight_data_List:
            t = "Partida: {} Destino: {} Saida: {}  Chegada: {} Aeronave: {} {} - Velocidade Aprox.: {} KM/h - Valor por KM: BRL {}"
            print(t.format(a1, a2, f.departure_time, f.arrival_time, f.aircraftManufacturer, f.aircraft, f.avgSpeed, f.farePerKM))
