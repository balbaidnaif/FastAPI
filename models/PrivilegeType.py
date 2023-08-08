from tortoise.fields import CharField, UUIDField
from tortoise.fields import ForeignKeyField, ForeignKeyRelation
from tortoise.models import Model

from .Company import Company


class PrivilegeType(Model):
    id = UUIDField(pk=True)
    name = CharField(max_length=50)
    company: ForeignKeyRelation[Company] = ForeignKeyField(
        "models.Company", related_name=False)
