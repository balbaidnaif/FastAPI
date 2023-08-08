from typing import List

from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from models.Rider import Rider
from models.schemas import Rider_Pydantic, RiderIn_Pydantic, Coord
from routers.auth import TokenData, get_current_token

router = APIRouter()


@router.get("/", response_model=List[Rider_Pydantic])
async def get_riders(current_user: TokenData=Depends(get_current_token)):
    return await Rider_Pydantic.from_queryset(Rider.all())


@router.get("/{rider_id}", response_model=Rider_Pydantic)
async def get_rider(rider_id: str, current_user: TokenData=Depends(get_current_token)):
    try:
        rider = await Rider_Pydantic.from_queryset_single(Rider.get(id=rider_id))
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Rider {rider_id} not found")
    return rider




@router.post("/")
async def create_rider(rider: RiderIn_Pydantic, current_user: TokenData=Depends(get_current_token)):
    rider_obj = {"company_id": current_user.company_id, **rider.dict()}
    return await Rider.create(**rider_obj)


@router.put("/{rider_id}", )
async def update_rider(rider_id: str, rider: RiderIn_Pydantic, urrent_user: TokenData=Depends(get_current_token)):
    is_updated = await Rider.filter(id=rider_id).update(
        **rider.dict(exclude_unset=True))
    if not is_updated:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail=f"Rider {rider_id} not found")
    return "Updated Successfully"


@router.delete("/{rider_id}")
async def delete_rider(rider_id: str, urrent_user: TokenData=Depends(get_current_token)):
    deleted_rider = await Rider.filter(id=rider_id).delete()

    if not deleted_rider:
        raise HTTPException(
            status_code=404, detail=f"Rider {rider_id} not found")
    return "Successfully Deleted"
