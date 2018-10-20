from django.contrib import admin

from main.models import User, Plate, Synchronization

admin.site.register(User)
admin.site.register(Plate)
admin.site.register(Synchronization)
