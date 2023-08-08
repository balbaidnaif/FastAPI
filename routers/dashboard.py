from typing import List

from asyncpg.pgproto.pgproto import UUID
from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from logic.estimation_time_model import training, estimation_time, dummy_data
from logic.genaral_logic import replace_uuid_with_str
from models.BusAccount import BusAccount
from models.CustomTrip import CustomTrip
from models.schemas import CustomTrip_Pydantic
from models.ConnectionManager import ConnectionManager
# from models.schemas import DashboardWaiters
# from routers.auth import get_current_token
from models.schemas import BusAccount_Pydantic
from routers.user_socket import managers

router = APIRouter()

@router.post("/")
async def test():
    await dummy_data(50, managers[0].tracks['elements'])
@router.get("/")
async def testModel():


    obj = await CustomTrip_Pydantic.from_queryset(CustomTrip.all())



    return len(obj)