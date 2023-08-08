from typing import List

from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from models.Station import Station
from models.schemas import Station_Pydantic, StationIn_Pydantic
from routers.auth import get_current_token

router = APIRouter()


@router.get("/", response_model=List[Station_Pydantic])
async def get_stations(current_user=Depends(get_current_token)):
    return await Station_Pydantic.from_queryset(Station.all())


@router.get("/{station_id}", response_model=Station_Pydantic)
async def get_station(station_id: str, current_user=Depends(get_current_token)):

    try:
        station = await Station_Pydantic.from_queryset_single(Station.get(id=station_id))
        print(station.dict()["name"])
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Station {station_id} not found")
    return station


@router.post("/",)
async def create_station(station: StationIn_Pydantic, current_user=Depends(get_current_token)):
    station_obj = {"company_id": current_user.company_id, **station.dict()}
    return await Station.create(**station_obj)


@router.put("/{station_id}", )
async def update_station(station_id: str, station: StationIn_Pydantic, current_user=Depends(get_current_token)):
    is_updated = await Station.filter(id=station_id).update(
        **station.dict(exclude_unset=True))
    if not is_updated:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail=f"Station {station_id} not found")

    return "Updated Successfully"


@router.delete("/{station_id}")
async def delete_station(station_id: str, current_user=Depends(get_current_token)):
    deleted_station = await Station.filter(id=station_id).delete()
    if not deleted_station:
        raise HTTPException(
            status_code=404, detail=f"station {station_id} not found")
    return "Deleted Successfully"
