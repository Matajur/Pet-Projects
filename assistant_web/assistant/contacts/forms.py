from datetime import date

from django.core.exceptions import ValidationError
from django.forms import (
    ModelForm,
    CharField,
    EmailField,
    DateField,
    DateInput,
    TextInput,
)
from .models import Contact
from phonenumber_field.formfields import PhoneNumberField


class ContactForm(ModelForm):
    name = CharField(
        max_length=20,
        required=True,
        widget=TextInput(attrs={"placeholder": "obligatory field"}),
    )
    thurname = CharField(max_length=20, required=False)
    address = CharField(max_length=100, required=False)
    phone = PhoneNumberField(
        required=False,
        widget=TextInput(attrs={"placeholder": "ex. +4402031234567"}),
    )
    email = EmailField(max_length=50, required=False)
    birthdate = DateField(
        required=False,
        widget=DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = Contact
        fields = (
            "name",
            "thurname",
            "address",
            "phone",
            "email",
            "birthdate",
        )

    def clean_birthdate(self):
        """
        The clean_birthdate function is a custom validation function that checks if the birthdate entered by the user is valid.
            It first gets the data from cleaned_data dictionary and then checks if it's not None. If it's not None, then we check
            whether or not it's in future or older than 100 years old. If any of these conditions are met, we raise an error.

        :param self: Access the instance of the class
        :return: A date object
        :doc-author: Trelent
        """
        data = self.cleaned_data.get("birthdate")
        print(data)
        today = date.today()
        if data is not None:
            if data > today:
                raise ValidationError("Birthdate cannot be in future")
            elif (today - data).days > (365 * 100):
                raise ValueError("User cannot be older than 100 years")
            return data
