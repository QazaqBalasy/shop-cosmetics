from django.core.validators import RegexValidator

ZIP_CODE_VALIDATOR = RegexValidator(
    regex="^[0-9]{2}-[0-9]{3}$", message="You need to provide valid zip code"
)

PHONE_NUMBER_VALIDATOR = RegexValidator(
    regex="^[+]?[0-9-\s]+$", message="You need to provide valid phone number"
)
