from random import randint
from django.http import JsonResponse
from django.shortcuts import render

from client.settings import SECRET_KEY, BASE_DIR
from main.models import User, Plate


def encode(password):
    from hashlib import sha224
    return sha224((SECRET_KEY + password).encode('utf-8')).hexdigest()


def sign_in(request):
    password = encode(request.POST.get('password'))
    try:
        user = User.objects.get(login=request.POST.get('login'),
                                        password=password)
        if not user.token:
            user.token = encode("{0}{1}{2}".format(str(user.id), '-', str(randint(0, 1023))))
        user.save()
        request.session['token'] = user.token
        return user.token
    except:
        return None


def update_token(request):
    try:
        user = User.objects.get(token=request.session['token'])
        user.token = encode("{0}{1}{2}".format(str(user.id), '-', str(randint(0, 1023))))
        user.save()
        request.session['token'] = user.token
        return True
    except:
        return False


def render_authorization_page(request):
    return render(request,
                  BASE_DIR + '/main/templates/authorization.html')
