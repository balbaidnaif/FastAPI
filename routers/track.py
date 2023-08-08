from typing import List

from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from models.Station import Station
from models.Track import Track
from models.schemas import Track_Pydantic, TrackIn_Pydantic, Station_Pydantic
from routers.auth import get_current_token, TokenData
# from models.Station import Station

router = APIRouter()


@router.get("/", response_model=List[Track_Pydantic])
async def get_tracks(current_user=Depends(get_current_token)):
    return await Track_Pydantic.from_queryset(Track.all())


@router.get("/{track_id}", response_model=Track_Pydantic)
async def get_track(track_id: str, current_user=Depends(get_current_token)):
    try:
        track = await Track_Pydantic.from_queryset_single(Track.get(id=track_id).prefetch_related("station"))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Track {e} not found")
    return track


@router.post("/",)
async def create_track(track: TrackIn_Pydantic, current_user: TokenData=Depends(get_current_token)):
    # print(track.dict())
    # print("===============")
    track_obj= await Track.create(name= track.name, coord= track.coord, color= track.color, start_time= track.start_time, end_time= track.end_time, company_id=current_user.company_id, interval=track.interval)
    # await track_obj.station.add(*track.stations)
    stations = []
    for station in track.stations:
        station_obj = await Station.get(id=station)
        stations.append(station_obj)
    await track_obj.station.add(*stations)
    return track_obj



@router.put("/{track_id}", )
async def update_track(track_id: str, track: TrackIn_Pydantic, current_user: TokenData=Depends(get_current_token)):
    track_obj = {"company_id": current_user.company_id, **track.dict()}
    is_updated = Track.filter(id=track_id).update(
        **track.dict())
    if not is_updated:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail=f"Track {track_id} not found")

    return "Updated Successfully"


@router.delete("/{track_id}")
async def delete_track(track_id: str, current_user=Depends(get_current_token)):
    deleted_track = await Track.filter(id=track_id).delete()

    if not deleted_track:
        raise HTTPException(
            status_code=404, detail=f"Track {track_id} not found")
    return "Deleted Successfully"
