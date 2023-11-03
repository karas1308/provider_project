from django import forms

from account.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["password", "phone"]
