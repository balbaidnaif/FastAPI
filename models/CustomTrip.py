from tortoise.fields import ForeignKeyField, ForeignKeyRelation, CharField
from tortoise.fields import UUIDField, DatetimeField, IntField
from tortoise.models import Model
from .Station import Station


class CustomTrip(Model):
    id = UUIDField(pk=True)
    start_hour = IntField()
    start_min = IntField()
    estimation_time_in_seconds = IntField()
    waiting_riders = IntField()

    distance = IntField()
    start_station: ForeignKeyRelation[Station] = ForeignKeyField(
        "models.Station", related_name=False)
    end_station: ForeignKeyRelation[Station] = ForeignKeyField(
        "models.Station", related_name=False)
    day = CharField(max_length=20)
