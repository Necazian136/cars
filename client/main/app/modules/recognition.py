import os

from main.models import Plate, User
from client.settings import BASE_DIR


def recognize(file):
    import car_recognition as cr
    return cr.recognize(BASE_DIR + '/pictures/' + file)


def check_number(request, recognized_plates):
    token = request.session['token']
    ok = False
    for recognized_plate in recognized_plates:
        if request.POST.get('only_main') == 'on':
            recognized_plate = recognized_plate.split(' ')[0]
            if any(recognized_plate.lower() == plate.number.split(' ')[0].lower()
                   for plate in Plate.objects.filter(user_id=User.objects.get(token=token).id)):
                ok = True
        else:
            if any(recognized_plate.lower() == plate.number.lower()
                   for plate in Plate.objects.filter(user_id=User.objects.get(token=token).id)):
                ok = True
    return ok


def load_image(request):
    if len(os.listdir(BASE_DIR + '/pictures/')) != 0:
        cnt = int(max(os.listdir(BASE_DIR + '/pictures/'), key=lambda x: int(x.split('.')[0])).split('.')[0])
        cnt += 1
    else:
        cnt = 0
    f = open(BASE_DIR + '/pictures/' + str(cnt) + '.jpg', 'wb')
    f.write(request.FILES['image'].read())
    f.close()
    return str(cnt) + '.jpg'


def delete_image(file):
    os.remove(BASE_DIR + '/pictures/' + file)
