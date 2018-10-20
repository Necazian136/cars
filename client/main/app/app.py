from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from main.models import User
from main.app.modules import user, sync, profile, recognition


def api(request):
    if request.method == 'GET':
        try:
            User.objects.get(token=request.session['token'])
            return profile.render_profile_page(request, {'plates': profile.get_plates(request)})
        except:
            return user.render_authorization_page(request)
    elif request.method == 'POST':
        return eval(request.POST.get('method') + '(request)')
    else:
        return HttpResponseBadRequest


def sign_in(request):
    if user.sign_in(request):
        context = {'plates': profile.get_plates(request)}
        return profile.render_profile_page(request, context)
    return user.render_authorization_page(request)


def register_plate(request):
    try:
        if profile.check_plate(request.POST.get('plate_number')):
            if profile.register_plate(request):
                sync.put(request)
                sync.synchronize(request)
                return profile.render_profile_page(request, {'plates': profile.get_plates(request)})
            return profile.render_profile_page(request, {'plates': profile.get_plates(request),
                                                         'error': 'already exists'})
    except:
        pass
    return profile.render_profile_page(request, {'plates': profile.get_plates(request),
                                                 'error': 'wrong number'})


def delete_plate(request):
    try:
        profile.delete_plate(request)
        sync.put(request)
        sync.synchronize(request)
    except:
        pass
    return profile.render_profile_page(request, {'plates': profile.get_plates(request)})


def recognize(request):
    file_name = recognition.load_image(request)
    recognized_plates = recognition.recognize(file_name)
    recognition.delete_image(file_name)
    context = {}
    context['plates'] = profile.get_plates(request)
    if recognition.check_number(request, recognized_plates):
        context['recognized'] = True
    else:
        context['recognized'] = False
    return profile.render_profile_page(request, context)


@csrf_exempt
def synchronize(request):
    sync.synchronize(request)
    return HttpResponse(True)


@csrf_exempt
def is_online(request):
    return HttpResponse(True)

















