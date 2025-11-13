import uuid
from django.db import models


def generate_token():
    return str(uuid.uuid4()).replace("-", "")


class TokenField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 32)
        kwargs.setdefault("editable", False)
        kwargs.setdefault("default", generate_token)
        super(TokenField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = super(TokenField, self).pre_save(model_instance, add)
        if not value:
            value = generate_token()
            setattr(model_instance, self.attname, value)
        return value
