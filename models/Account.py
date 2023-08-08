from tortoise.fields import ForeignKeyField, ForeignKeyRelation, CharField
from tortoise.fields import UUIDField
from tortoise.models import Model

from .Company import Company


class Account(Model):
    id = UUIDField(pk=True)
    role = CharField(max_length=50)
    company: ForeignKeyRelation[Company] = ForeignKeyField(
        "models.Company", related_name=False)

    class PydanticMeta:
        exclude = ("company", "company_id")
