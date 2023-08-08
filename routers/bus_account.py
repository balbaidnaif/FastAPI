
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from models.BusAccount import BusAccount
from models.schemas import BusAccount_Pydantic, BusAccountIn_Pydantic
from routers.auth import get_current_token, TokenData

router = APIRouter()


# ###################### Define Routes ###################### #

# Get All BusAccounts
@router.get("/", response_model=List[BusAccount_Pydantic])
async def get_bus_accounts(current_user=Depends(get_current_token)):
    return await BusAccount_Pydantic.from_queryset(BusAccount.all())


# Get A BusAccount
@router.get("/{bus_account_id}", response_model=BusAccount_Pydantic)

async def get_bus_account(bus_account_id: str, current_user=Depends(get_current_token)):
    try:
        bus_account_obj = await BusAccount_Pydantic.from_queryset_single(BusAccount.get(id=bus_account_id))
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"BusAccount {bus_account_id} not found")

    return bus_account_obj


# Create A BusAccount
@router.post("/")
async def create_bus_account(bus_account: BusAccountIn_Pydantic, current_user: TokenData =Depends(get_current_token)):
    bus_obj = {"company_id": current_user.company_id, "role": "bus", **bus_account.dict()}

    return await BusAccount.create(**bus_obj)


# Edit A BusAccount
@router.put("/{bus_account_id}")
async def update_bus_account(bus_account_id: str, bus_account: BusAccountIn_Pydantic, current_user=Depends(get_current_token)):
    is_updated = await BusAccount.filter(id=bus_account_id).update(**bus_account.dict())

    if not is_updated:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail=f"BusAccount {bus_account_id} not found")
    return "Updated Successfully"


# Delete A BusAccount
@router.delete("/{bus_account_id}")
async def delete_bus_account(bus_account_id: str, current_user=Depends(get_current_token)):
    is_deleted = await BusAccount.filter(id=bus_account_id).delete()
    if not is_deleted:
        raise HTTPException(status_code=403, detail=f"BusAccount {bus_account_id} not found")
    return "Deleted Successfully"
