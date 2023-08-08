# pip install geopy
from typing import List

import numpy as np
import geopy.distance as Distance

from models.Station import Station
from models.schemas import Station_Pydantic

track = [[50, 40], [51, 41], [51.55, 41.22]]
my_point = [50.22, 40.55]
destination = [51.55, 41.22]

# to get the nearest point to my location in the passed array
# @param my_location as list [lat,lng], points_arr as 2d list [[lat, lng],[lat, lng]]
# will return "nearest_point" as tuple (lat, lng) , "distance" between them in meters


def nearest_point_2me(my_location, points_arr):
    nearest_point = None
    distance = None
    my_loc = [my_location.get("lat"), my_location.get("lng")]

    points_arr = np.array((points_arr))
    my_loc = np.array((my_loc))
    print(points_arr.dtype, my_loc.dtype)
    sum_sq = np.sum(np.square(points_arr - my_loc), axis=1)

    index_of_nearest = np.argmin(sum_sq)

    nearest_point = points_arr[index_of_nearest]

    my_point = tuple(my_loc)
    nearest_point = tuple(nearest_point)
    distance = Distance.distance(my_point, nearest_point).m

    print(nearest_point)
    print(distance)
    return nearest_point, distance

# print(nearest_point_2me(my_point,track))


bus_location = [3, 3]
track = {
    "name": "Path 1",
    "color": "#000000",
    "start_time": "2022-2-19",
    "end_time": "2022-3-19",
    "station": [
        {
            "id": "0764209c-0e0e-4b82-8800-4f40d4a9fdf3",
            "name": "new station",
            "coord": {
                "lat": 26.315291225608345,
                "lng": 50.14820086995314
            }
        },
        {
            "id": "725cbb74-c353-4719-bfdd-5fa97721c5f7",
            "name": "844",
            "coord": {
                "lat": 26.314451,
                "lng": 50.145331
            }
        },
        {
            "id": "ae7125dd-e7bb-47b7-b43d-caa0d1f8bb94",
            "name": "68",
            "coord": {
                "lat": 26.313093,
                "lng": 50.14464
            }
        },
        {
            "id": "6f8683f3-3ae0-4d0d-8c16-be21421382e7",
            "name": "naifs station",
            "coord": {
                "lat": 124,
                "lng": 123
            }
        },
        {
            "id": "f6caf13a-7b98-4886-885b-b1a2b76dc849",
            "name": "naifs station",
            "coord": {
                "lat": 124,
                "lng": 123
            }
        }
    ],
    "coord": [
        {
            "lat": 26.315291225608345,
            "lng": 50.14820086995314,
            "originalIndex": 0,
            "interpolated": False
        },
        {
            "lat": 3,
            "lng": 4,
            "interpolated": True
        },
        {
            "lat": 5,
            "lng": 5,
            "interpolated": True
        },
        {
            "lat": 26.313675699999997,
            "lng": 50.1444908,
            "interpolated": True
        },
        {
            "lat": 26.313675699999997,
            "lng": 50.1444908,
            "interpolated": True
        },
        {
            "lat": 26.313873899999997,
            "lng": 50.145253499999995,
            "interpolated": True
        },
        {
            "lat": 26.313888799999997,
            "lng": 50.14528500000001,
            "interpolated": True
        },
        {
            "lat": 26.313901499999997,
            "lng": 50.145302,
            "interpolated": True
        },
        {
            "lat": 26.313093,
            "lng": 50.14464,
            "interpolated": False
        },
        {
            "lat": 26.313926300000002,
            "lng": 50.1453212,
            "interpolated": True
        },
        {
            "lat": 26.3139487,
            "lng": 50.1453254,
            "interpolated": True
        },
        {
            "lat": 26.3140061,
            "lng": 50.145310200000004,
            "interpolated": True
        },
        {
            "lat": 26.3143856,
            "lng": 50.145193299999995,
            "interpolated": True
        },
        {
            "lat": 26.3143856,
            "lng": 50.145193299999995,
            "interpolated": True
        },
        {
            "lat": 26.314419538187146,
            "lng": 50.14534005520997,
            "originalIndex": 1,
            "interpolated": False
        }
    ]
}


# to get the total distance between my location (roughly) and the destination in meter
# (depends on the track)

# @param start_location as coord, destination as coord
# track as track object
# will return "total_distance" between them in meters depends on the track
def distance_between_2points_in_track(start_location, destination, track):

    total_distance = 0.0
    print(track)

    coord = track.get("coord")
    lats = [
        lat for e in coord
        if (lat := e.get('lat')) is not None
    ]
    lngs = [
        lng for e in coord
        if (lng := e.get('lng')) is not None
    ]
    track_latlngs = np.column_stack((lats, lngs))
    start_point, _ = nearest_point_2me(start_location, track_latlngs)
    # print(start_point,'nearest point in track')
    print(destination,"destna")
    destination, _ = nearest_point_2me(destination, track_latlngs)


    destination = np.array((destination))

    print(destination,"destna")
    start_point = np.array((start_point))
    print(track_latlngs,"latlongs")
    print(start_point, "point")
    start_index = np.where((track_latlngs[:, 0] == start_point[0]) & (
        track_latlngs[:, 1] == start_point[1]))[0]
    print(start_index)
    end_index = np.where((track_latlngs[:, 0] == destination[0]) & (
        track_latlngs[:, 1] == destination[1]))[0]
    print(end_index)
    # print(start_index[0], end_index[0],"range")

    if (start_index[0] > end_index[0]):
        for i in range(start_index[0], len(track_latlngs)-1):
            dis = Distance.distance(tuple(track_latlngs[i]), tuple(track_latlngs[i+1])).m
            total_distance = total_distance + dis
        for i in range(0, start_index[0]):
            dis = Distance.distance(
                tuple(track_latlngs[i]), tuple(track_latlngs[i+1])).m
            total_distance = total_distance + dis

    else:
        for i in range(start_index[0], end_index[0]):
            dis = Distance.distance(
                tuple(track_latlngs[i]), tuple(track_latlngs[i+1])).m
            total_distance = total_distance + dis

    return total_distance


# to get the previous and the next stations depending on bus_location in a specific track
# it will return the next_station_id in string as will as prev_station_id
# @param "track" object from the Back-end , "bus_location" as list [lat, lng]
def previous_and_next_stations(track, bus_location):
    prev_station_id = ""
    next_station_id = ""
    prev = []
    next = []

    # get lats and lngs from the track
    coord = track.get("coord")
    lats = [
        lat for e in coord
        if (lat := e.get('lat')) is not None
    ]
    lngs = [
        lng for e in coord
        if (lng := e.get('lng')) is not None
    ]

    # combine lats and lngs and get the nearest point in the track
    track_latlngs = np.column_stack((lats, lngs))
    nearest_point, _ = nearest_point_2me(bus_location, track_latlngs)


    nearest_point = np.array(nearest_point)
    # print(nearest_point,"nearest point")
    print(nearest_point, "bus nearest")

    # to differentiate from stations and helper point
    is_station = [
        lat for e in coord
        if (lat := e.get('lat') and e.get('originalIndex') != None) is not None
    ]
    track_info = np.column_stack((track_latlngs, is_station))

    # get the information about current point (the nearest to bus_location)
    current_index = np.where((track_info[:, 0] == nearest_point[0]) & (
        track_info[:, 1] == nearest_point[1]))[0]
    current_point = track_info[current_index]

    print(track_info, "track info")

    # if the current point is station ==> it will be consedred as prev
    if(current_point[0][2] == 1.0):
        print("i am true")
        prev = current_point[0][0:2]
    else:
        station = 0
        index = current_index[0]
        while (station != 1 and index > 0):
            index -= 1
            if (index < 0):
                index = track_info.shape[0]-1
                # print('index should == ',track_info.shape[0])
            prev_point = track_info[[index]]
            if(prev_point[0][2] == 1.0):
                prev = prev_point[0][0:2]
                station = 1
    print(prev, "prev")
    index = current_index[0]
    is_station = 0

    while (is_station != 1 and index < len(track_info)):
        index += 1
        # print(index)
        # print(track_info.shape)
        if (index >= track_info.shape[0]):
            index = 0
            # print('index should == ',0)
        next_point = track_info[[index]]
        if(next_point[0][2] == 1.0):
            next = next_point[0][0:2]
            print(next, "next")
            is_station = 1

    stations = track.get('station')
    # print(next)
    prev_s = {"lat": prev[0], "lng": prev[1]}
    next_s = {"lat": next[0], "lng": next[1]}
    prev_station, _ = nearest_station_2me(track["station"], prev_s)
    next_station, _ = nearest_station_2me(track["station"], next_s)



    # for station in stations:
    #     # print(station.get("coord").get('lat'), "laat")
    #     print(station.get("coord").get('lat'), prev[0], "is round up")
    #     print(station.get("coord").get('lat') == prev[0], "is round up")
    #
    #     if (station.get("coord").get('lat') == prev[0] and
    #             station.get("coord").get('lng') == prev[1]):
    #         prev_station = station
    #     if (station.get("coord").get('lat') == next[0] and
    #             station.get("coord").get('lng') == next[1]):
    #         next_station = station
    print(prev_station, next_station, "prev and next")
    return prev_station, next_station

# sample of output = ('0764209c-0e0e-4b82-8800-4f40d4a9fdf3', 'ae7125dd-e7bb-47b7-b43d-caa0d1f8bb94')

# print(previous_and_next_stations(track, bus_location))


my_location = {"lat": 4, "lng": 4}
list_of_stations = [{
    "id": "1",
    "name": "string",
    "coord": {"lat": 1, "lng": 5}
},
    {
    "id": "2",
    "name": "string",
    "coord": {"lat": 5, "lng": 5}
}]


# to get the nearest station to my location
# @param list_of_stations as list of station objects, my_location as object
# will return "nearest_station_id" string , "distance" between them in meters

def nearest_station_2me(list_of_stations, my_location):
    # get lats and lngs for the stations
    lats = []
    lngs = []
    for i in range(len(list_of_stations)):

        lats.append(float(list_of_stations[i].get('coord').get("lat")))
        lngs.append(float(list_of_stations[i].get('coord').get("lng")))

    # get the nearest station (lat, lng) and the distance to it

    stations_latlngs = np.column_stack((lats, lngs))

    nearest_point, distance = nearest_point_2me(my_location, stations_latlngs)

    # to return the id of the nearest station (not just [lat, lng])

    for i in range(len(list_of_stations)):
        if (float(list_of_stations[i].get("coord").get("lat")) == nearest_point[0] and
                float(list_of_stations[i].get("coord").get("lng")) == nearest_point[1]):
            nearest_station = list_of_stations[i]
            # print(nearest_station, distance)
            return nearest_station, distance

# print(nearest_station_2me(list_of_stations, my_location))


# to get the nearest station to my location
# @param station_coord as {lat:000 , lng:000}, tracks_pass_station as list of track objects
# @param list_of_all_buses as list of bus objects
# will return list of 5 nearest_buses sorted descending

def nearest_buses_2_station(station, tracks_pass_station, list_of_all_buses):
    nearest_buses = []
    print(station, 'inside nearest buses function')
    print(list_of_all_buses, "inside nearest buss function")
    for track in tracks_pass_station:
        buses_pass_station = list(
            filter(lambda bus: track['id'] == bus["track_id"], list_of_all_buses))
        print(buses_pass_station,"busses pass")
        for bus in buses_pass_station:
            dist = distance_between_2points_in_track(bus.get("coord"), station, track)
            nearest_buses.append([bus, dist])

    nearest_buses.sort(key=lambda row: (row[1]))
    return nearest_buses[0]
