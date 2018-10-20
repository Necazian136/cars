from django.contrib import admin
from django.urls import path
from main.app import app

urlpatterns = [
    path('', app.api),
    path('status/', app.is_online),
    path('synchronization/', app.synchronize),
    path('admin/', admin.site.urls),
]
