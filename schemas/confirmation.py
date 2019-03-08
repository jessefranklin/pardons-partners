from ma import ma
from models.confirmation import ConfirmationModel


class ConfirmationSchema(ma.ModelSchema):
    class Meta:
        model = ConfirmationModel
        load_only = ("user",)
        dump_only = ("id", "expired_ad", "confirmed")
        include_fk = True