from datetime import datetime
from random import random
from typing import List
import json
from starlette.websockets import WebSocket

from logic.estimation_time_model import estimation_time
from logic.genaral_logic import get_filtered_list, replace_uuid_with_str, get_number_of_waiters, set_number_of_waiters
from logic.estimation_time_to_user import nearest_station_2me, previous_and_next_stations, \
    distance_between_2points_in_track, nearest_buses_2_station
from models.BusAccount import BusAccount
from models.BusLocationData import BusLocationData
from models.CustomTrip import CustomTrip
from models.RiderLocationData import RiderLocationData
from models.Station import Station
from models.schemas import Track, Track_Pydantic, Station, Station_Pydantic, Coord, BusAccount_Pydantic
from models.UserConnection import UserConnection
from logic.estimation_time_to_user import nearest_station_2me

buses = [{"id": "12346", }]


class ConnectionManager:
    def __init__(self, company_id: str):
        self.company_id: str = company_id
        self.active_connections: List[UserConnection] = []
        self.busses = {"type": "buses", "elements": []}
        self.riders = {"type": "riders", "elements": []}
        self.tracks = {"type": "tracks", "elements": []}
        self.stations = {"type": "stations", "elements": []}
        # self.buses: List[BusAccount_Pydantic]
        print('initiate manager')

    async def connect(self, websocket: WebSocket, client_id: str, type: str):
        await websocket.accept()
        await websocket.send_json(self.busses)
        await websocket.send_json(self.riders)
        await websocket.send_json(self.stations)
        await websocket.send_json(self.tracks)
        if type == "bna":
            await websocket.send_json(self.get_dashboard_data())
        user = UserConnection(client_id, type, websocket)
        self.active_connections.append(user)
        return user

    async def get_data(self):
        tracks = await Track_Pydantic.from_queryset(Track.filter(company_id=self.company_id))
        stations = await Station_Pydantic.from_queryset(Station.filter(company_id=self.company_id))
        for track in tracks:
            new_track = replace_uuid_with_str(track.dict())
            self.tracks.get("elements").append(new_track)
        for station in stations:
            new_station = replace_uuid_with_str(station.dict())
            new_station["waiters"] = 0
            self.stations.get("elements").append(new_station)
        # for bus in busses:
        #     bus_obj = bus.dict()
        #     bus_obj.pop('track')
        #     new_bus = replace_uuid_with_str(bus_obj)
        #     self.busses.get("elements").append(new_bus)

    def disconnect(self, user_connection: UserConnection):
        self.active_connections.remove(user_connection)

    def set_destination(self, coord: Coord, destination: Station_Pydantic, model):
        tracks_pass_destination = list()
        print(destination)
        for track in self.tracks["elements"]:
            # tracks_pass_destination.extend(list(filter(lambda station: destination["id"] == station.id, track.station)))
            for station in track["station"]:
                if (station["id"] == destination["id"]):
                    tracks_pass_destination.append(track)
                    break
        print(tracks_pass_destination, "------ tracks_pass_dest")
        # tracks_pass_destination = self.fun(destination)
        # print(self.tracks)
        # print(tracks_pass_destination)
        stations = list()
        for track in tracks_pass_destination:
            for station in track["station"]:
                if station not in stations:
                    stations.append(station)

        # print(stations,"---- sations should contains the dest")

        nearest_station = nearest_station_2me(list(stations), coord)
        print(nearest_station[0], "nearest station to user")

        tracks_pass_nearest_station = list()
        for track in tracks_pass_destination:
            for station in track['station']:
                if station['id'] == nearest_station[0]['id']:
                    if track not in tracks_pass_nearest_station:
                        tracks_pass_nearest_station.append(track)
                        break

        # print("here1")
        # print(nearest_station)
        # print(self.get_busses(), "busses --------------------------")

        # print(tracks_pass_nearest_station, len(tracks_pass_destination), "track pass nearest")
        buses = self.get_busses()

        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        nearest_bus = nearest_buses_2_station(nearest_station[0]["coord"], tracks_pass_nearest_station,
                                              buses["elements"])
        print(nearest_bus, "-----------------------------------Nearest bus")

        bus_track = None

        for track in tracks_pass_nearest_station:
            if track["id"] == nearest_bus[0]["track_id"]:
                bus_track = track

        # print(bus_track)
        previous_station, next_station = previous_and_next_stations(bus_track, nearest_bus[0]['coord'])

        distance = distance_between_2points_in_track(nearest_bus[0]['coord'], next_station["coord"], bus_track)
        # start_station, distance = nearest_station_2me(self.stations, nearest_bus[0]['coord'])
        next_station = get_number_of_waiters(next_station, self.stations['elements'])
        previous_station = get_number_of_waiters(previous_station, self.stations['elements'])
        waiters = next_station["waiters"]
        now = datetime.now()
        day_name = now.strftime("%A").lower()
        if previous_station == nearest_station[0]:
            print("inside if")
            status = "to destination"
            data = [previous_station["id"], next_station["id"], distance, waiters, now.hour, now.minute, day_name]
            total_time = estimation_time(data, model)
            # Runs the model to destination.
            while not previous_station["id"] == destination["id"]:
                print("Inside while loop")

                previous_station, next_station = previous_and_next_stations(nearest_bus[0]['track'],
                                                                            next_station['coord'])
                distance = distance_between_2points_in_track(previous_station["coord"], next_station["coord"],
                                                             nearest_bus[0]["track"])
                now = datetime.now()
                data = [previous_station["id"], next_station["id"], distance, waiters, now.hour, now.minute,
                        day_name]
                total_time += estimation_time(data, model)

        else:

            status = "to me"
            data = [previous_station["id"], next_station["id"], distance, waiters, now.hour, now.minute, day_name]
            total_time = estimation_time(data, model)
            print(previous_station["id"] == nearest_station[0]['id'],
                  "========================================================================================================")
            while not previous_station["id"] == nearest_station[0]['id']:
                print("inside loop 2")
                print(nearest_bus[0])
                nearest_bus_track = list(filter(lambda track: nearest_bus[0]['track_id'] == track['id'], self.tracks['elements']))[0]
                previous_station, next_station = previous_and_next_stations(nearest_bus_track,
                                                                            next_station['coord'])
                distance = distance_between_2points_in_track(previous_station["coord"], next_station["coord"],
                                                             nearest_bus_track)
                now = datetime.now()
                data = [previous_station["id"], next_station["id"], distance, waiters, now.hour, now.minute, day_name]
                total_time += estimation_time(data, model)
        print({"nearest_bus": nearest_bus[0], "nearest_station": nearest_station[0], "total_time": total_time[0],
               "status": status})
        results = {"nearest_bus": nearest_bus[0], "nearest_station": nearest_station[0], "total_time": total_time[0],
                   "status": status, 'type': "start-trip"}
        return results

    async def update_estimation_time(self, bus, nearest_station, destination, model):
        bus_track = list(filter(lambda track: bus['track_id'] == track['id'], self.tracks['elements']))
        bus_track = bus_track[0]
        previous_station, next_station = previous_and_next_stations(bus_track, bus['coord'])

        distance = distance_between_2points_in_track(bus['coord'], next_station["coord"], bus_track)
        # start_station, distance = nearest_station_2me(self.stations, bus['coord'])
        next_station = get_number_of_waiters(next_station, self.stations['elements'])
        previous_station = get_number_of_waiters(previous_station, self.stations['elements'])
        waiters = next_station["waiters"]
        now = datetime.now()
        day_name = now.strftime("%A").lower()
        if previous_station == nearest_station[0]:
            status = "to destination"
            data = [previous_station["id"], next_station["id"], distance, waiters, now.hour, now.minute, day_name]
            total_time = estimation_time(data, model)
            total_distance = distance_between_2points_in_track(bus['coord'], destination["coord"], bus_track)

            # Runs the model to destination.
            while not previous_station["id"] == destination["id"]:
                previous_station, next_station = previous_and_next_stations(bus_track,
                                                                            next_station['coord'])
                distance = distance_between_2points_in_track(previous_station["coord"], next_station["coord"],
                                                             bus_track)
                now = datetime.now()
                data = [previous_station["id"], next_station["id"], distance, waiters, now.hour, now.minute,
                        day_name]
                total_time += estimation_time(data, model)

        else:

            status = "to me"
            data = [previous_station["id"], next_station["id"], distance, waiters, now.hour, now.minute, day_name]
            total_time = estimation_time(data, model)
            while not previous_station["id"] == nearest_station[0]['id']:
                previous_station, next_station = previous_and_next_stations(bus_track,
                                                                            next_station['coord'])
                distance = distance_between_2points_in_track(previous_station["coord"], next_station["coord"],
                                                             bus_track)
                now = datetime.now()
                data = [previous_station["id"], next_station["id"], distance, waiters, now.hour, now.minute, day_name]
                total_time += estimation_time(data, model)
        print({"nearest_bus": bus_track, "nearest_station": nearest_station, "total_time": total_time,
               "status": status})
        results = {"nearest_bus": bus_track, "nearest_station": nearest_station[0], "total_time": total_time[0],
                   "status": status, type: "update-trip"}
        return results

    def get_dashboard_data(self):
        average_track_time = []
        for track in self.tracks['elements']:
            print('test')

            average_track_time.append({
                'id': str(track.get('id')),
                'name': track.get('name'),
                'time': int(random()*4)
            })
            print(average_track_time)
        return ({
            'type': 'average_track_time',
            'elements': average_track_time
        })

    async def update_emulated_bus(self, data, websocket: WebSocket):
        found = False
        for bus in self.busses['elements']:
            if data["account_id"] == bus["id"]:
                bus['coord'] = data['coord']
                bus['time'] = data['time']
                found = True
                break

        if (not found):
            print('crate new bus , not found')

            bus_dict = dict()
            bus_dict['id'] = data['id']
            bus_dict["coord"] = data["coord"]
            bus_dict["time"] = data["time"]
            self.busses["elements"].append(bus_dict)

        for connection in self.active_connections:
            if not connection.type == "arduino":
                await connection.websocket.send_json(self.busses)

    async def update_bus_location(self, data, websocket: WebSocket):

        try:
            saved_bus = None
            found = False
            for bus in self.busses['elements']:
                if data["account_id"] == bus["id"]:
                    saved_bus = bus
                    bus['coord'] = data['coord']
                    bus['time'] = data['time']
                    found = True
                    break

            print(self.get_busses())
            if (not found):
                print('crate new bus , not found')

                bus = await BusAccount_Pydantic.from_queryset_single(BusAccount.get(id=data["account_id"]))
                bus_dict = bus.dict()
                bus_dict["coord"] = data["coord"]
                bus_dict["time"] = data["time"]
                saved_bus = replace_uuid_with_str(bus_dict)
                self.busses["elements"].append(saved_bus)
            # else:
            #     saved_bus["coord"] = data["coord"]
            #     saved_bus["track_id"] = data["track_id"]
            #     saved_bus["time"] = data["time"]


            if 'trip' in saved_bus and saved_bus['trip']["end_time"] is None:
                print('trip is still running')
                distance = distance_between_2points_in_track(saved_bus['coord'],
                                                             saved_bus['trip']['next_station_coord'],
                                                             self.tracks[1].dict())
                print('distance to reach')
                print(distance)
                saved_bus["trip"]['distance'] = int(distance)
                if (distance < 20):
                    saved_bus["trip"]['waiting_riders'] = 2
                    saved_bus['trip']["estimation_time_in_seconds"] = int(saved_bus['time']) - int(
                        saved_bus['trip']['start_time']),
                    saved_bus["trip"].pop('next_station_coord')
                    saved_bus["trip"].pop('start_time')
                    saved_bus["trip"].pop('end_time')

                    await CustomTrip.create(start_hour=saved_bus['trip']['start_hour'],
                                            start_min=saved_bus['trip']['start_min'],
                                            estimation_time_in_seconds=saved_bus['trip']['estimation_time_in_seconds'][
                                                0], distance=saved_bus['trip']['distance'],
                                            start_station_id=saved_bus['trip']['start_station'],
                                            end_station_id=saved_bus['trip']['end_station'],
                                            waiting_riders=saved_bus['trip']['waiting_riders'])
                    saved_bus['trip']['status'] = 'saved'
                    print('trip saved successfully')

                    saved_bus.pop('trip')

            if data.get('type') == "start_trip":
                print('trip has started')
                prev_station, next_station = previous_and_next_stations(self.tracks[0].dict(),
                                                                        data['coord'])
                print(prev_station)
                print(next_station)
                saved_bus['trip'] = {"start_time": data["time"],
                                     'start_hour': datetime.now().hour,
                                     'start_min': datetime.now().minute,
                                     "end_time": None,
                                     "start_station": str(prev_station["id"]),
                                     "end_station": str(next_station["id"]),
                                     "next_station_coord": next_station["coord"],
                                     }
                print(saved_bus["trip"])

            for connection in self.active_connections:
                if not connection.type == "arduino":
                    await connection.websocket.send_json(self.busses)

            await BusLocationData.create(**data)
            # self.busses["elements"] = get_filtered_list(self.busses["elements"])

        except Exception as e:
            print("Data is not valid")
            print(e)

    def get_busses(self):
        return self.busses

    async def update_rider_location(self, data, websocket: WebSocket):
        try:
            # print('here1')
            found = False

            # print(data['coord'])
            nearest_station = nearest_station_2me(self.stations['elements'], data['coord'])
            # print(nearest_station)
            for rider in self.riders['elements']:
                if data["account_id"] == rider["account_id"]:
                    rider['account_id'] = data["account_id"]
                    rider['coord'] = data['coord']
                    rider['time'] = data['time']
                    if nearest_station[1] < 20:
                        rider["station"] = nearest_station[0]["id"]
                    else:
                        rider["station"] = None
                    found = True
                    break

            if not found:
                saved_rider = {"account_id": data["account_id"], "coord": data["coord"], "time": data["time"]}
                if nearest_station[1] < 20:
                    saved_rider["station"] = nearest_station[0]["id"]
                else:
                    saved_rider["station"] = None
                self.riders["elements"].append(saved_rider)
            for connection in self.active_connections:
                if not connection.type == "arduino":
                    await connection.websocket.send_json(self.riders)
            set_number_of_waiters(self.riders['elements'], self.stations['elements'])
            self.riders["elements"] = get_filtered_list(self.riders["elements"])
        except Exception as e:
            print(e)
