import requests

import datetime
import dateutil.parser
from zeep import Client

API_KEY = "2e7f2092-fa93-4661-947c-e09444d5bd26"  # TODO get in a file
#API_KEY_NAVITIA = "f2e975ad-24a8-4c0a-9d0c-0c9c230531d9"

url = "https://api.sncf.com/v1/coverage/sncf/journeys?from=admin:fr:75056&to=admin:fr:69123&datetime=20190124T100549"

CITY_TO_DISTANCE_SOAP_URL = "http://soapwebserviceusmb.azurewebsites.net:80/services/HelloWorld?wsdl"
PRICE_URL = "https://fathomless-ridge-71475.herokuapp.com/kmToPrice/"
DIVISE = "euro"


def format_datetime(date: datetime) -> str:
    res = f"{date.year:04d}{date.month:02d}{date.day:02d}T{date.hour:02d}{date.minute:02d}{date.second:02d}"
    return res


def list_stations(page):
    return requests.get(f"https://ressources.data.sncf.com/api/records/1.0/search/"
                        f"?dataset=liste-des-gares&start={page}")


def timetable(gare_start_code, gare_stop_code, time_start, count=10, page=0):
    print(time_start)
    req = f"https://api.sncf.com/v1/coverage/sncf/journeys?from={gare_start_code}&to={gare_stop_code}&datetime={time_start}&count={count}"
    print(req)
    return requests.get(req, auth=(API_KEY, ""))


def get_station_id(station_name):
    res = requests.get(f"https://api.sncf.com/v1/coverage/sncf/places?q={station_name}", auth=(API_KEY, ""))
    return res.json()["places"][0]["id"]   # TODO  check if place exists


def get_station_coordinate(station_name):  # FIXME cache result ??
    res = requests.get(f"https://api.sncf.com/v1/coverage/sncf/places?q={station_name}", auth=(API_KEY, ""))
    place = res.json()["places"][0]
    coordinate = place["administrative_region"]["coord"]
    return coordinate["lat"], coordinate["lon"]


def get_trains(from_city, to_city, date):
    from_city_id = get_station_id(from_city)
    to_city_id = get_station_id(to_city)
    res_timetable = timetable(from_city_id, to_city_id, format_datetime(date.astimezone()))
    return res_timetable.json()


def get_distance(from_city, to_city):
    lat1, long1 = get_station_coordinate(from_city)
    lat2, long2 = get_station_coordinate(to_city)
    client = Client(CITY_TO_DISTANCE_SOAP_URL)  # TODO use singleton
    result = client.service.getPrice(lat1, long1, lat2, long2)
    return float(result)


def get_price(distance):
    res = requests.get(f"{PRICE_URL}{DIVISE}/{distance}")
    return res.json()["price"]


def get_journey_price(from_city, to_city):
    distance = get_distance(from_city, to_city)
    print(distance)
    price = get_price(distance)
    return price


if __name__ == '__main__':
    # my_list_stations = list_stations(0).json()
    # print(my_list_stations)
    # print(my_list_stations["records"][0]["fields"])
    # fromPlace = get_station_id("chambery")
    # toPlace = get_station_id("annecy")
    # resTimetable = timetable(fromPlace, toPlace, datetime.datetime.now().isoformat(), 0)
    # myJson = resTimetable.json()
    # print(myJson)
    # for travel in myJson["journeys"]:
    #     departure = dateutil.parser.parse(travel['departure_date_time'])
    #     arrival = dateutil.parser.parse(travel['arrival_date_time'])
    #     print(f"duration : {travel['duration'] / 60} minutes, departure : {departure}, arrival : {arrival}")

    distance = get_distance("annecy", "chambé")
    print(distance)

    price = get_journey_price("annecy", "chambé")
    print(price)
