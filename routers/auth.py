from datetime import datetime, timedelta, date
from typing import List, Optional

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
from models.BNA import BNA
from models.BusAccount import BusAccount
from models.schemas import BNAIn_Pydantic, BNA_Pydantic

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 999999


class Token(BaseModel):
    access_token: str
    token_type: str
    bus_account_id: str = None

class RiderData(BaseModel):
    rider_id: str
    company_id: str

class TokenData(BaseModel):
    user_id: Optional[str] = None
    company_id: Optional[str] = None
    role: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)

router = APIRouter()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str):
    user = await BNA.get(username=username)
    print("================")
    print(user.password)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:

        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=999999)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def read_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get("user_id")
        company_id: str = payload.get("company_id")
        role: str = payload.get("role")

        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id, company_id=company_id, role=role)
        return token_data
    except:
        raise credentials_exception


async def get_current_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get("user_id")
        company_id: str = payload.get("company_id")
        role: str = payload.get("role")

        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id, company_id=company_id,role=role)
    except:
        raise credentials_exception

    return token_data


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": str(user.id), "company_id": str(user.company_id), "role": str(user.role), "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    if(user.role == 'bus_driver'):
        try:
            bus_account: BusAccount = await BusAccount.get(driver= user.id)
            return {"access_token": access_token, "token_type": "bearer", "bus_account_id":str(bus_account.id)}
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This driver is not linked to any bus account')

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login_for_access_token(rider: RiderData):

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": rider.rider_id, "company_id": str(rider.company_id), "role": 'rider'},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/get_hash")
async def get_hash(form_data: OAuth2PasswordRequestForm = Depends()):
    new_hash = get_password_hash(form_data.password)
    return new_hash


@router.post("/register")
# Create A BNA
async def create_bna(bna: BNAIn_Pydantic,current_user=Depends(get_current_token)):
    bna.password = get_password_hash(bna.password)
    bna_obj = {"company_id": current_user.company_id, **bna.dict()}
    return await BNA.create(**bna_obj)
    return user


@router.get("/token",)
async def read_users_me(current_user=Depends(get_current_token)):
    return current_user