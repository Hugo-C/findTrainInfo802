import requests

import datetime
import dateutil.parser

API_KEY = "2e7f2092-fa93-4661-947c-e09444d5bd26"  # TODO get in a file
#API_KEY_NAVITIA = "f2e975ad-24a8-4c0a-9d0c-0c9c230531d9"

url = "https://api.sncf.com/v1/coverage/sncf/journeys?from=admin:fr:75056&to=admin:fr:69123&datetime=20190124T100549"


def format_datetime(date: datetime) -> str:
    return f"{date.year}{date.month}{date.day}T{date.hour}{date.minute}{date.second}"


def list_stations(page):
    return requests.get(f"https://ressources.data.sncf.com/api/records/1.0/search/"
                        f"?dataset=liste-des-gares&start={page}")


def timetable(gare_start_code, gare_stop_code, time_start, page=0):
    req = f"https://api.sncf.com/v1/coverage/sncf/journeys?from={gare_start_code}&to={gare_stop_code}&datetime={time_start}"
    print(req)
    return requests.get(req, auth=(API_KEY, ""))


def get_station_id(station_name):
    res = requests.get(f"https://api.sncf.com/v1/coverage/sncf/places?q={station_name}", auth=(API_KEY, ""))
    return res.json()["places"][0]["id"]   # TODO  check if place exists


def getTains(from_city, to_city):
    res = []
    from_city_id = get_station_id(from_city)
    to_city_id = get_station_id(to_city)
    res_timetable = timetable(from_city_id, to_city_id, datetime.datetime.now().isoformat())
    return res_timetable.json()


if __name__ == '__main__':
    # my_list_stations = list_stations(0).json()
    # print(my_list_stations)
    # print(my_list_stations["records"][0]["fields"])
    fromPlace = get_station_id("chambery")
    toPlace = get_station_id("annecy")
    resTimetable = timetable(fromPlace, toPlace, datetime.datetime.now().isoformat(), 0)
    myJson = resTimetable.json()
    print(myJson)
    for travel in myJson["journeys"]:
        departure = dateutil.parser.parse(travel['departure_date_time'])
        arrival = dateutil.parser.parse(travel['arrival_date_time'])
        print(f"duration : {travel['duration'] / 60} minutes, departure : {departure}, arrival : {arrival}")
