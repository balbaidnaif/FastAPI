from typing import List

from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from models.PrivilegeType import PrivilegeType
from models.schemas import PrivilegeType_Pydantic, PrivilegeTypeIn_Pydantic
from routers.auth import get_current_token

router = APIRouter()


@router.get("/", response_model=List[PrivilegeType_Pydantic])
async def get_privileges(current_user=Depends(get_current_token)):
    return await PrivilegeType_Pydantic.from_queryset(PrivilegeType.all())


@router.get("/{privilege_id}", response_model=PrivilegeType_Pydantic)
async def get_privilege(privilege_id: str, current_user=Depends(get_current_token)):
    try:
        privilege = await PrivilegeType_Pydantic.from_queryset_single(id=privilege_id)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"PrivilegeType {privilege_id} not found")

    return privilege


@router.post("/", response_model=PrivilegeType_Pydantic)
async def create_privilege(privilege: PrivilegeTypeIn_Pydantic, current_user=Depends(get_current_token)):
    privilege = await PrivilegeType.create(**privilege.dict())
    return "Created Successfully"


@router.put("/{privilege_id}", )
async def update_privilege(privilege_id: str, privilege: PrivilegeTypeIn_Pydantic, current_user=Depends(get_current_token)):
    is_updated = await PrivilegeType.filter(id=privilege_id).update(
        **privilege.dict(exclude_unset=True))
    if not is_updated:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail=f"PrivilegeType {privilege_id} not found")

    return "Updated Successfully"


@router.delete("/{privilege_id}")
async def delete_privilege(privilege_id: str, current_user=Depends(get_current_token)):
    deleted_privilege = await PrivilegeType.filter(id=privilege_id).delete()

    if not deleted_privilege:
        raise HTTPException(
            status_code=404, detail=f"Privilege {privilege_id} not found")
    return "Successfully Deleted"
