from typing import List

from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from models.BNA import BNA
from routers.auth import get_current_token, TokenData

from models.schemas import BNA_Pydantic, BNAIn_Pydantic

router = APIRouter()


# ###################### Define Routes ###################### #

# Get All BNAs
@router.get("/", response_model=List[BNA_Pydantic])
async def get_bna():
    return await BNA_Pydantic.from_queryset(BNA.exclude(role='bus_driver'))


# Get A BNA by ID
@router.get("/{bna_id}", response_model=BNA_Pydantic)
async def get_bna(bna_id: str, current_user=Depends(get_current_token)):
    try:
        bna_obj = await BNA_Pydantic.from_queryset_single(BNA.get(id=bna_id))
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"BusAccount {bna_id} not found")

    return bna_obj


# Create A BNA
@router.post("/",)
async def create_bna(bna: BNAIn_Pydantic, current_user: TokenData =Depends(get_current_token)):
    bna_obj = {"company_id": current_user.company_id, **bna.dict()}

    return await BNA.create(**bna_obj)


# Edit A BNA
@router.put("/{bna_id}", )
async def update_bna(bna_id: str, bna: BNAIn_Pydantic,current_user=Depends(get_current_token)):
    is_updated = await BNA.filter(id=bna_id).update(**bna.dict(exclude_unset=True))

    if not is_updated:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED,current_user=Depends(get_current_token), detail=f"BusAccount {bna_id} not found")
    return "Updated Successfully"


# Delete A BNA
@router.delete("/{bna_id}",)
async def delete_bna(bna_id: str, current_user=Depends(get_current_token)):
    is_deleted = await BNA.get(id=bna_id).delete()
    if not is_deleted:
        raise HTTPException(status_code=403, detail=f"bna {bna_id} not found")
    return "Deleted Successfully"
