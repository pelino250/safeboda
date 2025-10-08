from django.contrib import admin

from users.models import User, Passenger, Rider

admin.site.register(User)
admin.site.register(Passenger)
admin.site.register(Rider)