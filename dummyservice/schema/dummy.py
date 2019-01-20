from ma import ma
from models.dummy import DummyModel

class DummySchema(ma.ModelSchema):
    class Meta:
        model = DummyModel
        dumpy_only = ("id",)
