from tortoise.fields import ForeignKeyField, ForeignKeyRelation, ManyToManyField, ManyToManyRelation
from tortoise.fields import UUIDField, DatetimeField
from tortoise.fields.data import CharField, JSONField, IntField
from tortoise.models import Model

from .Company import Company
from .Station import Station


class Track(Model):
    id = UUIDField(pk=True)
    name = CharField(max_length=50)
    station: ManyToManyRelation[Station] = ManyToManyField(
        "models.Station", related_name="tracks")
    coord = JSONField(null=True)
    color = CharField(50)
    company: ForeignKeyRelation[Company] = ForeignKeyField(
        "models.Company", related_name=False)
    start_time = CharField(max_length=50)
    end_time = CharField(max_length=50)
    interval = IntField()

    class PydanticMeta:
        exclude = ("company", "company_id")
