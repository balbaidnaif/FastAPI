from tortoise.fields import OneToOneField, OneToOneNullableRelation, CharField, ForeignKeyField

from models.Account import Account
from models.BNA import BNA


class BusAccount(Account):
    name = CharField(max_length=50, null=True)
    driver: OneToOneNullableRelation[BNA] = OneToOneField(
        "models.BNA", related_name=False, null=True)
    track= ForeignKeyField("models.Track", related_name=False)

    class PydanticMeta:
        exclude = ("company", "role", "company_id")