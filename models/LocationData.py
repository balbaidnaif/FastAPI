from tortoise import Model
from tortoise.fields import DatetimeField, ForeignKeyField, ForeignKeyRelation, JSONField, UUIDField

from .Company import Company


class LocationData(Model):
    id = UUIDField(pk=True)
    coord = JSONField()
    time = DatetimeField()
    company: ForeignKeyRelation[Company] = ForeignKeyField(
        "models.Company", related_name=False)


    class PydanticMeta:
        exclude = ("company", "company_id")

    # async def update_location(self, data, manager):
    #     location = await self.create(**data.dict())
    #     for connection in manager.active_connections:
    #         if not connection.type == "arduino":
    #             await connection.websocket.send_json(data)
