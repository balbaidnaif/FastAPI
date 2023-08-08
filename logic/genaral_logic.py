from datetime import datetime
from typing import List

from asyncpg.pgproto.pgproto import UUID

from models.Station import Station
from models.schemas import Station_Pydantic, Rider_Pydantic, StationIn_Pydantic


def get_filtered_list(elements):
    now = datetime.now().timestamp()
    return list(filter(lambda element: now - element.get("time") <= 70, elements))


def set_number_of_waiters(riders, stations):
    for station in stations:
        number_of_waiters = len(list(filter(lambda rider: rider['station'] == station["id"], riders)))
        station["waiters"] = number_of_waiters

def get_number_of_waiters(curr_station, stations):
    print(curr_station, "get number of waiters")
    print(stations)
    station_obj = list(filter(lambda station: station['id'] == curr_station["id"], stations))
    return station_obj[0]

def replace_uuid_with_str(object: dict):
    for key in object.keys():
        if isinstance(object[key], UUID):
            object[key] = str(object[key])
        elif isinstance(object[key], dict):
            replace_uuid_with_str(object[key])
        elif isinstance(object[key], list):
            for element in object[key]:
                replace_uuid_with_str(element)
    return object
