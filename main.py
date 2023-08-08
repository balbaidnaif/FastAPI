from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from database.database import init_db
from routers.auth import router as auth_router
from routers.bna import router as bna_router
from routers.bus_account import router as bus_account_router
from routers.company import router as company_router
from routers.rider import router as rider_router
from routers.station import router as station_router
from routers.track import router as track_router
from routers.user_socket import router as socket_router
from routers.bus_driver import router as bus_driver_router
from routers.custom_trip import router as custom_trip_router
from routers.dashboard import router as dashboard

app = FastAPI()

origins = [
    "http://swe-417.herokuapp.com",
    "https://swe-417.herokuapp.com",
    "https://masaar-project.netlify.app",
    "http://masaar-project.netlify.app",
    "http://localhost",
    "http://localhost:3000",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Start DB Connection on Startup
app.include_router(company_router, tags=["Company"], prefix="/company")
app.include_router(bus_account_router, tags=[
    "BusAccount"], prefix="/busaccount")
app.include_router(bna_router, tags=["BNA"], prefix="/bna")

app.include_router(rider_router, tags=["Rider"], prefix="/rider")
app.include_router(station_router, tags=["Station"], prefix="/station")
app.include_router(track_router, tags=["Track"], prefix="/track")
app.include_router(socket_router, tags=["Socket"], prefix="/socket")
app.include_router(auth_router, tags=["Auth"], prefix="/auth")
app.include_router(bus_driver_router, tags=["BusDriver"], prefix="/busdriver")
app.include_router(custom_trip_router, tags=["CustomTrip"], prefix="/customtrip")
app.include_router(dashboard, tags=["Dashboard"], prefix="/dashboard")

@app.on_event("startup")
async def startup_event():
    init_db(app)
