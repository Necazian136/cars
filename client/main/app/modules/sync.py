import json

from django.http import JsonResponse, HttpResponseBadRequest, QueryDict

from main.models import User, Plate, Synchronization
from client.settings import BASE_DIR
from pip._vendor import requests
import ast
from main.app import app


def put(request):
    user = User.objects.get(token=request.session['token'])
    sync_data = {'method': request.POST.get('method'),
                 'plate_number': request.POST.get('plate_number')}
    s = Synchronization(request=str(sync_data),
                        user_id=user.id)
    s.save()

def synchronize(request):
    f = open(BASE_DIR + '/server_ip.txt')
    server_url = f.read().split('\n')[0].split('=')[1]
    f.close()
    user = User.objects.get(id=1)
    s = Synchronization.objects.filter(user_id=user.id)
    sync_data = ''
    for i in s:
        sync_data += i.request + '|'
    try:
        response = requests.post('http://' + server_url + ':8000/synchronization/',
                                 {'login': user.login,
                                  'password': user.password,
                                  'requests': str(sync_data)}).json()['response']
    except:
        response = False
    if response:
        Synchronization.objects.filter(user_id=user.id).delete()
        for r in response:
            r =ast.literal_eval(r)
            q = QueryDict('', mutable=True)
            q.update(r)
            request.POST = q
            request.session['token'] = user.token
            if r['method'] == 'register_plate':
                app.register_plate(request)
            if r['method'] == 'delete_plate':
                app.delete_plate(request)
    return True
