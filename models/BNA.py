from tortoise.fields import CharField

from .Account import Account


class BNA(Account):
    username = CharField(max_length=50,unique= True )
    password = CharField(max_length=255)

    class PydanticMeta:
        exclude = ("company", "company_id")
