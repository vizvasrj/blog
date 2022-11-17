from django.db import models

class LowercaseEMailField(models.EmailField):
    # overriding email field to lowercase
    def to_python(self, value):
        # COnvert email to validate
        value = super(LowercaseEMailField, self).to_python(value)
        if isinstance(value, str):
            return value.lower()
        return value


class LowercaseUsernameField(models.CharField):
    def to_python(self, value):
        value = super(LowercaseUsernameField, self).to_python(value)
        if isinstance(value, str):
            return value.lower()
        return value