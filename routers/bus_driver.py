from random import randint
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from models.BNA import BNA
from models.schemas import BusDriver_Pydantic, BusDriverIn_Pydantic
from routers.auth import get_current_token

router = APIRouter()


# ###################### Define Routes ###################### #

# Get All BNAs
@router.get("/", response_model= List[BusDriver_Pydantic])
async def get_bus_drivers(current_user=Depends(get_current_token)):

    return await BusDriver_Pydantic.from_queryset(BNA.filter(role='bus_driver', company_id=current_user.company_id))


# Get A BNA
@router.get("/{bus_driver_id}", response_model=BusDriver_Pydantic)
async def get_bus_driver(bus_driver_id: str, current_user=Depends(get_current_token)):
    try:
        bus_driver_obj = await BusDriver_Pydantic.from_queryset_single(BNA.get(id=bus_driver_id))
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"BusAccount {bus_driver_id} not found")

    return bus_driver_obj


# Create A BNA
@router.post("/", )
async def create_bus_driver(bus_driver: BusDriverIn_Pydantic, current_user=Depends(get_current_token)):

    generated_password = '123456'
    bus_driver_obj = {"company_id": current_user.company_id, "role": "bus_driver", "password": str(generated_password), **bus_driver.dict()}
    await BNA.create(**bus_driver_obj)
    return generated_password


# Edit A BNA
@router.put("/{bus_driver_id}", )
async def update_bus_driver(bus_driver_id: str, bus_driver: BusDriverIn_Pydantic, current_user=Depends(get_current_token)):
    is_updated = await BNA.filter(id=bus_driver_id).update(**bus_driver.dict(exclude_unset=True))

    if not is_updated:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail=f"BusAccount {bus_driver_id} not found")
    return "Updated Successfully"


# Delete A BNA
@router.delete("/{bus_driver_id}")
async def delete_bus_driver(bus_driver_id: str, current_user=Depends(get_current_token)):
    is_deleted = await BNA.filter(id=bus_driver_id).delete()
    if not is_deleted:
        raise HTTPException(status_code=403, detail=f"BNA {bus_driver_id} Not Found")
    return "Deleted Successfully"


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)