
from django import forms


class UserForm(forms.Form):
    """Форма пользователя"""
    class Meta:
        pass
    #fields = ('username', 'password', 'email')

    username = forms.CharField(max_length=32, label='Имя пользователя')
    email = forms.CharField(max_length=40, label='Email')
    password = forms.CharField(max_length=40, label='Пароль')
    name = forms.CharField(max_length=40, label='Наименование')
    inn = forms.CharField(max_length=20, label='ИНН')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)