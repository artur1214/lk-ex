import json

import requests
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect


# Create your views here.
from cabinet.forms import UserForm
from cabinet.models import Profile


def index(request):
    return render(request, 'index.html')

def user_login(request):
    def post():
        if request.user.is_authenticated:
            return JsonResponse({'success': True})
        else:
            username = request.POST.get('username', False)
            password = request.POST.get('password', False)
            print(username)
            user = Profile.auth(username, password)
            if isinstance(user, User):
                login(request, user)
                return JsonResponse({'success': True})
            else:
                print(user)
                return JsonResponse({'success': False})

    return post() if request.method == 'POST' \
        else HttpResponseForbidden('403 Method not Allowed')

def user_register(request):
    def post():
        #print(request.)
        print(request.body)
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            user = Profile.register(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'],
                                    email=form.cleaned_data['email'],
                                    inn=form.cleaned_data['inn'],
                                    name=form.cleaned_data['name']
                                    )
            if isinstance(user[0], Profile):
                login(request, user[0].user)
                return JsonResponse({'success': True})
            else:
                return JsonResponse(user[0])
        return JsonResponse(form.errors)


    return post() if request.method == 'POST' \
        else HttpResponseForbidden('403 Method not Allowed')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('/cabinet/')
    return render(request, 'registration.html', {'form': UserForm})


def get_cabinet_link(priceplan_id):
    SUBDOMAIN = "test"
    LOGIN_TPL = f'http://{SUBDOMAIN}-lk.pp.ru:8000/api/login'
    AUTH_KEY_GEN = \
        f'http://{SUBDOMAIN}-lk.pp.ru:8000/api/clients/%s/auth-key/'

    REDIRECT_LINK = f'http://{SUBDOMAIN}-lk.pp.ru:8000/auth-key/%s/'
    session = requests.session()
    payload_manager = {
        'user': 'priceplan',
        'password': 'priceplan'
    }

    rsp_login = session.post(LOGIN_TPL, data=json.dumps(payload_manager))
    user_id = str(priceplan_id)  # id Клиента в системе priceplan, полученный где-то выше
    rsp_auth_key = session.post(AUTH_KEY_GEN % user_id)  # создание ссылки

    auth_data = json.loads(rsp_auth_key.content)
    print(auth_data)
    priceplan_auth_key = auth_data['data']['key']  # получение auth_key
    return REDIRECT_LINK % priceplan_auth_key


def cabinet_view(request):
    if not request.user.is_authenticated:
        return redirect('/register/')
    link = get_cabinet_link(request.user.profile.priceplan_id)
    return render(request, 'cabinet.html', {'user': request.user, 'cabinet_link': link})

def redirect_to_pp(request):
    return redirect()
