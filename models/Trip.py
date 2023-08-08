from tortoise.fields import ForeignKeyField, ForeignKeyRelation
from tortoise.fields import UUIDField, DatetimeField
from tortoise.models import Model

from .Company import Company
from .Rider import Rider


class Trip(Model):
    id = UUIDField(pk=True)
    start_time = DatetimeField()
    end_time = DatetimeField()
    rider: ForeignKeyRelation[Rider] = ForeignKeyField("models.Rider", related_name=False)
    company: ForeignKeyRelation[Company] = ForeignKeyField(
        "models.Company", related_name=False)
