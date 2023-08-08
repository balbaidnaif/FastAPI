from typing import List

from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends

from logic.estimation_time_model import training
from logic.estimation_time_to_user import previous_and_next_stations
from models.BusLocationData import BusLocationData
from models.ConnectionManager import ConnectionManager
from models.RiderLocationData import RiderLocationData
from models.Station import Station
from models.Track import Track
from routers.auth import get_current_token, TokenData, read_token

router = APIRouter()

managers: List[ConnectionManager] = []


@router.websocket("/{client_id}")
async def user_socket(websocket: WebSocket, client_id: str, user_type: str, token: str):
    current_user: TokenData = await read_token(token)
    model = await training()
    company_manager = None
    for current_manager in managers:
        if current_manager.company_id == current_user.company_id:
            company_manager = current_manager
            break

    if (company_manager == None):
        company_manager = ConnectionManager(current_user.company_id)
        await company_manager.get_data()

        managers.append(company_manager)

    user_connection = await company_manager.connect(websocket, current_user.user_id, user_type)

    while True:
        try:
            data = await websocket.receive_json()
            data = {"account_id": current_user.user_id, "company_id": current_user.company_id, **data}
            print('received data from ' + company_manager.company_id)

            if user_type == "bus":
                await company_manager.update_bus_location(data, websocket)

            elif user_type == "rider":
                if data.get("type") == "start_trip":
                    await websocket.send_json(company_manager.set_destination(data["coord"], data["station"], model))
                else:
                    await company_manager.update_rider_location(data, websocket)

            elif user_type == "bna":
                if data["type"] == "dashboard":
                    await company_manager.get_dashboard_data(data, websocket)
                elif data["type"] == "update":
                    await company_manager.update_bus_location(data, websocket)
                elif data["type"] == "rider_emulator":
                    await company_manager.update_rider_location(data, websocket)

        except WebSocketDisconnect:
            company_manager.disconnect(user_connection)
