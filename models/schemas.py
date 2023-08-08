from typing import List

from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel
from models.BNA import BNA
from models.BusAccount import BusAccount
from models.BusLocationData import BusLocationData
from models.Company import Company
from models.CustomTrip import CustomTrip
from models.LocationData import LocationData
from models.PrivilegeType import PrivilegeType
from models.Rider import Rider
from models.RiderLocationData import RiderLocationData
from models.Station import Station
from models.Track import Track

BusAccount_Pydantic = pydantic_model_creator(
    BusAccount, name="BusAccount", exclude=["company", "company_id", "driver", "track"], )

BusAccountIn_Pydantic = pydantic_model_creator(
    BusAccount, name="BusAccountIn", exclude_readonly=True)

BNAIn_Pydantic = pydantic_model_creator(BNA, name="BNAIn", exclude_readonly=True)
BNA_Pydantic = pydantic_model_creator(BNA, name="BNA", exclude=["company","password", "company_id"])

BusDriverIn_Pydantic = pydantic_model_creator(BNA, name="BusDriverIn", exclude=["role", "password"], exclude_readonly=True)
BusDriver_Pydantic = pydantic_model_creator(BNA, name="BusDriver", exclude=["company", "password", "role", "company_id"])


CompanyIn_Pydantic = pydantic_model_creator(Company, name="Company", exclude_readonly=True)
Company_Pydantic = pydantic_model_creator(Company, name="CompanyIn")

LocationData_Pydantic = pydantic_model_creator(
    LocationData, exclude=["company", "company_id"], name="LocationData")
LocationInData_Pydantic = pydantic_model_creator(
    LocationData, name="LocationInData", exclude_readonly=True)

BusLocationData_Pydantic = pydantic_model_creator(
    BusLocationData, name="BusLocationData", exclude=["track", "company", "company_id"])
BusLocationInData_Pydantic = pydantic_model_creator(
    BusLocationData, name="BusLocationDataInData", exclude_readonly=True)

RiderLocationData_Pydantic = pydantic_model_creator(
    RiderLocationData, name="RiderLocationData", exclude=[], )
RiderLocationInData_Pydantic = pydantic_model_creator(
    RiderLocationData, name="RiderLocationDataInData", exclude_readonly=True)

Rider_Pydantic = pydantic_model_creator(
    Rider, name="Rider", exclude=["company", "company_id"], )
RiderIn_Pydantic = pydantic_model_creator(
    Rider, name="RiderIn", exclude_readonly=True)

CustomTrip_Pydantic = pydantic_model_creator(
    CustomTrip, name="CustomTrip", exclude=["start_station", "end_station"])
CustomTripIn_Pydantic = pydantic_model_creator(
    CustomTrip, name="CustomTripIn", exclude_readonly=True)

Station_Pydantic = pydantic_model_creator(
    Station, name="Station", exclude=["tracks", "company_id", "company"])
StationIn_Pydantic = pydantic_model_creator(
    Station, name="StationIn", exclude_readonly=True)

Track_Pydantic = pydantic_model_creator(
    Track, name="Track", exclude=["company", "company_id"],)


class TrackIn_Pydantic(BaseModel):
    name: str
    stations: List[str]
    coord: List[dict]
    color: str
    start_time: str
    end_time: str
    interval: int

class Coord(BaseModel):
    lat: float
    lng: float

class DashboardWaiters(BaseModel):
    id = str
    name = str
    coord = Coord
    waiters = int


PrivilegeType_Pydantic = pydantic_model_creator(
    PrivilegeType, name="PrivilegeType", exclude=["company", "company_id"])
PrivilegeTypeIn_Pydantic = pydantic_model_creator(
    PrivilegeType, name="PrivilegeIn", exclude_readonly=True)