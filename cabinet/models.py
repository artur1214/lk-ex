import json

import requests
from django.db import models
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.db import models
from django.utils.crypto import get_random_string

class Profile(models.Model):
    """
    Поскольку Profile расширяет User (а не AbstractBaseUser или
    AbstractUser) не стоит определять его как AUTH_USER_MODEL.
    """

    class Meta:
        db_table = 'qq_profiles'
        app_label = "cabinet"
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    priceplan_id = models.IntegerField(null=True)

    @staticmethod
    def register(**kwargs):
        if 'username' in kwargs.keys() and 'password' in kwargs.keys() and \
                'email' in kwargs.keys():
            if User.objects.filter(username=kwargs['username']):
                return {'username': False}, False
            if User.objects.filter(email=kwargs['email']):
                return {'password': False}, False
            user = User.objects.create_user(
                username=kwargs['username'],
                password=kwargs['password']
            )
            user.first_name = kwargs['name']
            user.save()
            profile = Profile.objects.create(user=user)
            priceplan_id = Profile.create_priceplan_profile(kwargs['name'], kwargs['inn'], profile.id)
            profile.priceplan_id = priceplan_id
            profile.save()
            return profile, True
        return {}, False

    @staticmethod
    def create_priceplan_profile(name, inn, id):
        priceplan_url = 'http://test.pp.ru:8000/'

        session = requests.session()
        payload_manager = {
            'user': 'priceplan',
            'password': 'priceplan',
            'external_id': str(id)
        }

        rsp_login = session.post(priceplan_url+'api/login',
                                 data=json.dumps(payload_manager))
        new_user = session.post(priceplan_url + 'api/clients/',
                                data=json.dumps({
                                    'type': 1,
                                    'name': name,
                                    'signed_values':{
                                        'inn': inn,
                                        'external_id': str(id)
                                    }
                                }))
        print(new_user.content)
        new_user = json.loads(new_user.content)
        return new_user['data']['id']

    @classmethod
    def auth(cls, username, password):
        """Функция логинит пользователя
        Args:
            cls (Profile): Объект типа "класс Profile" (передается автоматически)
            username (str): Имя или email введенного пользователя
            password (str): Пароль введенного пользователя
        """
        try:
            user = cls.objects.get(user__username=username).user
        except cls.DoesNotExist:
            try:
                user = cls.objects.get(user__email=username).user
            except cls.DoesNotExist:
                return {'UserDoesNotExist': False}
        if check_password(password, user.password):
            return user
        else:
            return {'passwordError': False}
# Create your models here.
