from .LocationData import LocationData


riders = {"company""type": "riders", "elements": []}
class RiderLocationData(LocationData):
    pass


    class PydanticMeta:
        exclude = ("company", "company_id")
