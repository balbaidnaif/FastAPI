from websocket import WebSocket


class UserConnection:

    def __init__(self, id: str, type: str, websocket: WebSocket):
        self.websocket = websocket
        self.id = id
        self.type = type