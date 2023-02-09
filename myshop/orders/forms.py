from django import forms
from .models import Order

from localflavor.ru.forms import RUPostalCodeField
from localflavor.us.forms import USZipCodeField


class OrderCreateForm(forms.ModelForm):
    postal_code = RUPostalCodeField()

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
        labels = {"first_name": "Имя", "last_name": "Фамилия", "address": "Адрес",
                  "postal_code": "Почтовый индекс", "city": "Город"}
