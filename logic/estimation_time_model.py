import numpy as np
import geopy.distance as Distance
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# data = [{
#     "start_station": "string",
#     "distination_station": "string",
#     "distance_from_bus_to_dist": 350,
#     "num_of_waiting_in_distination": 20,
#     "hour": 10,
#     "min": 7,
#     "day": "wensday",
#     "estimation_time": 3,
# }, ...]
from models.CustomTrip import CustomTrip
from models.schemas import CustomTrip_Pydantic


async def data():
    return await CustomTrip.all()


# @param data is list of objects
async def training():
    try:
        data = await CustomTrip_Pydantic.from_queryset(CustomTrip.all())
        for i in range(len(data)):
            data[i] = data[i].dict()
            data[i]['start_station_id'] = str(data[i]['start_station_id'])
            data[i]['end_station_id'] = str(data[i]['end_station_id'])

        df = pd.DataFrame(data)

        y_data = df.estimation_time_in_seconds.values
        X_data = df[["start_station_id", "end_station_id", "day", "distance",
                    "waiting_riders", "start_hour", "start_min"]]
        print(X_data)
        OHE = OneHotEncoder()
        scaler = StandardScaler()
        lr = LinearRegression()

        cat_cols = ["start_station_id", "end_station_id", "day"]
        num_cols = ["distance",
                    "waiting_riders", "start_hour", "start_min"]

        transformer = ColumnTransformer([('cat_cols', OHE, cat_cols),
                                        ('num_cols', scaler, num_cols)])

        print(transformer)
        print(' step 1')
        pipe = Pipeline([("preprocessing", transformer),
                        ("classifier", lr)])
        print(' step 2')

        pipe2 = pipe.fit(X_data, y_data)
        print(' step 3')

        print(X_data)

        print("X_data---------------")
        return pipe2
    except:
        return 'error'


# data = [
#     "start_station", "distination_station", 350, 20, 10, 7, "wensday"
#  ]

# @param data as list
# @param model from training function
def estimation_time(data, model):
    list_name = data
    columns = ["start_station_id", "end_station_id", "distance",
               "waiting_riders", "start_hour", "start_min", "day"]
    print(list_name)
    df = pd.DataFrame([list_name], columns=columns)
    print(model)
    print('===============')
    print(df)
    print(' step 4')

    estimated_time = model.predict(df)
    print(' step 4')

    return estimated_time


import random
async def dummy_data(n,tracks):
    # {
    #     "start_hour": 2147483647,
    #     "start_min": 2147483647,
    #     "estimation_time_in_seconds": 2147483647,
    #     "waiting_riders": 2147483647,
    #     "distance": 2147483647,
    #     "day": "string",
    #     "end_station_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    #     "start_station_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    # }
    data =[]
    days = ["saturday","sunday","monday","tuesday","wednesday","thursday"]
    # days = ["saturday"]
    # for track in tracks:
    #     stations_ids = list(map(lambda station: station["id"], track["station"]))
    stations_ids = ['d83532b0-6fa8-4036-a9ee-02801e60e95c', "5c160718-14ca-4f19-8e19-ae1e1ca7cb20","ad3ef348-6eeb-4951-92c0-4bc88189e89e","d845797a-2465-4460-8eef-34759c4f207c"]
    for i in range(n):
        new = {}
        hour = random.randint(6, 16)
        new["start_hour"] = hour
        min = random.randint(0, 59)
        new["start_min"] = min
        estimation_time_in_seconds = random.randint(10, 120)
        new["estimation_time_in_seconds"] = estimation_time_in_seconds
        waiting_riders = random.randint(0, 30)
        new["waiting_riders"] = waiting_riders
        distance = random.randint(10,500)
        new["distance"] = distance
        day = days[random.randint(0,len(days)-1)]
        new["day"] = day
        station_index =random.randint(0,len(stations_ids)-1)


        if(station_index == len(stations_ids)-1):
            start_station_id = stations_ids[station_index]
            end_station_id = stations_ids[0]
        else:
            end_station_id =  stations_ids[station_index + 1]
            start_station_id = stations_ids[station_index]
        new["start_station_id"] = start_station_id
        new["end_station_id"] = end_station_id


        data.append(new)
        await CustomTrip.create(**new)


    return data
