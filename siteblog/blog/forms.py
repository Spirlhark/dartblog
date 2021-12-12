from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """Форма подписки по email"""
    class Meta:
        model = Contact
        fields = '__all__'


# class ContactEmail(forms.Form):
#     name = forms.CharField(max_length=30, label='Имя', required=False)
#     email = forms.EmailField(max_length=50, label='Почта')

