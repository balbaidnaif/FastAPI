from typing import List

from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from models.CustomTrip import CustomTrip
from models.schemas import CustomTrip_Pydantic, CustomTripIn_Pydantic
from routers.auth import TokenData, get_current_token

router = APIRouter()


@router.get("/", )
async def get_custom_trips(current_user: TokenData=Depends(get_current_token)):
    return await CustomTrip.all()

@router.get("/{custom_trip_id}", response_model=CustomTrip_Pydantic)
async def get_custom_trip(custom_trip_id: str, current_user: TokenData=Depends(get_current_token)):
    try:
        custom_trip = await CustomTrip_Pydantic.from_queryset_single(CustomTrip.get(id=custom_trip_id))
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"CustomTrip {custom_trip_id} not found")
    return custom_trip


@router.post("/")
async def create_custom_trip(custom_trip: CustomTripIn_Pydantic, current_user: TokenData=Depends(get_current_token)):

    return await CustomTrip.create(**custom_trip.dict())


@router.put("/{custom_trip_id}", )
async def update_custom_trip(custom_trip_id: str, custom_trip: CustomTripIn_Pydantic, urrent_user: TokenData=Depends(get_current_token)):
    is_updated = await CustomTrip.filter(id=custom_trip_id).update(
        **custom_trip.dict(exclude_unset=True))
    if not is_updated:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail=f"CustomTrip {custom_trip_id} not found")
    return "Updated Successfully"


@router.delete("/{custom_trip_id}")
async def delete_custom_trip(custom_trip_id: str, urrent_user: TokenData=Depends(get_current_token)):
    deleted_custom_trip = await CustomTrip.filter(id=custom_trip_id).delete()

    if not deleted_custom_trip:
        raise HTTPException(
            status_code=404, detail=f"CustomTrip {custom_trip_id} not found")
    return "Successfully Deleted"
