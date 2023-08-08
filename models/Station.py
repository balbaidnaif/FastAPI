from tortoise.fields import CharField, UUIDField, JSONField
from tortoise.fields import ForeignKeyField, ForeignKeyRelation
from tortoise.models import Model

from .Company import Company


class Station(Model):
    id = UUIDField(pk=True)
    name = CharField(max_length=50)
    coord = JSONField()
    company: ForeignKeyRelation[Company] = ForeignKeyField(
        "models.Company", related_name=False)

    class PydanticMeta:
        exclude = ("company", "company_id")

