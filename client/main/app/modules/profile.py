from django.shortcuts import render

from main.models import User, Plate
from client.settings import BASE_DIR


def render_profile_page(request, context={}):
    return render(request, BASE_DIR + '/main/templates/profile.html', context)


def register_plate(request):
    user = User.objects.get(token=request.session['token'])
    plates = Plate.objects.filter(user_id=user.id)
    plate_number = request.POST.get('plate_number')
    if not any(plate_number == p.number for p in plates):
        plate = Plate(number=plate_number, user_id=user.id)
        plate.save()
        return True
    return False


def check_plate(car_number):
    car_number = car_number.upper()
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    letters = ['А', 'В', 'Е', 'К', 'М', 'Н', 'О', 'Р', 'С', 'Т', 'У', 'Х']
    if len(car_number) > 5:
        if not any(car_number[0] == l for l in letters): return False
        if not any(car_number[1] == l for l in numbers): return False
        if not any(car_number[2] == l for l in numbers): return False
        if not any(car_number[3] == l for l in numbers): return False
        if not any(car_number[4] == l for l in letters): return False
        if not any(car_number[5] == l for l in letters): return False
        for i in range(7, len(car_number)):
            if not any(car_number[i] == l for l in numbers): return False
        return True
    return False


def delete_plate(request):
    user = User.objects.get(token=request.session['token'])
    plate = Plate.objects.get(number=request.POST.get('plate_number'), user_id=user.id)
    plate.delete()
    return True


def get_plates(request):
    user = User.objects.get(token=request.session['token'])
    plates = Plate.objects.filter(user_id=user.id)
    return plates
