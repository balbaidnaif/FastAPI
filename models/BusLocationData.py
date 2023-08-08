from cmath import log
import json
from tortoise.fields import BooleanField
from tortoise.fields import ForeignKeyField, ForeignKeyRelation

from .BusAccount import BusAccount
from .LocationData import LocationData
from .Track import Track

class BusLocationData(LocationData):
    account: ForeignKeyRelation[BusAccount] = ForeignKeyField(
        "models.BusAccount", related_name=False)
    track: ForeignKeyRelation[Track] = ForeignKeyField(
        "models.Track", related_name=False)

    class PydanticMeta:
        exclude = ("company", "company_id")




