from django.forms import ValidationError
from . import messages
import re


def mobile(value):
    reg = r"^09[0-9]{9}"
    if str:
        valid = re.match(reg, str(value))
        if not valid:
            raise ValidationError(message=messages.mobile_error_message)
