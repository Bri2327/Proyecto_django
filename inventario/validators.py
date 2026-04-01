from django.core.exceptions import ValidationError

def validatosr_par(value):
    if value % 2 != 0:
        raise ValidationError(f"{value} no es par")