from typing import List

from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from logic.estimation_time_model import training, estimation_time, data
from models.Company import Company
from models.schemas import Company_Pydantic, CompanyIn_Pydantic
from routers.auth import get_current_token

router = APIRouter()


# ###################### Define Routes ###################### #

# Get All Companies
@router.get("/", response_model=List[Company_Pydantic])
async def get_companies():
    return await Company_Pydantic.from_queryset(Company.all())


# Get A Company
@router.get("/{company_id}", response_model=Company_Pydantic)
async def get_company(company_id: str, current_user=Depends(get_current_token)):
    try:
        company_obj = await Company_Pydantic.from_queryset_single(Company.get(id=company_id))
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"BusAccount {company_id} not found")

    return company_obj


# Create A Company
@router.post("/")
async def create_company(company: CompanyIn_Pydantic, current_user=Depends(get_current_token)):
    await Company.create(**company.dict())

    return "Created Successfully"


# Edit A Company
@router.put("/{company_id}")
async def update_company(company_id: str, company: CompanyIn_Pydantic, current_user=Depends(get_current_token)):
    is_updated = await Company.filter(id=company_id).update(**company.dict(exclude_unset=True))

    if not is_updated:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail=f"BusAccount {company_id} not found")
    return "Updated Successfully"


# Delete A Company
@router.delete("/{company_id}")
async def delete_company(company_id: str, current_user=Depends(get_current_token)):
    is_deleted = await Company.filter(id=company_id).delete()
    if not is_deleted:
        raise HTTPException(status_code=403, detail=f"Company {company_id} not found")
    return "Deleted Successfully"

