from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r"^\+?1?\d{9,15}$",
    message="Номер должен быть в формате '+999999999'. До 15 цифр.",
)
