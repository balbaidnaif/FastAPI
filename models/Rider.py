from .Account import Account


class Rider(Account):
    pass


    class PydanticMeta:
        exclude = ("company", "company_id")