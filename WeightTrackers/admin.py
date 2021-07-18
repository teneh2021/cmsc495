

from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, Weight, Activities, Calculate, AddWeight, WeightTracker

# Register your models here.
#admin.site.unregister(User)
admin.site.register(WeightTracker)
#admin.site.register(User)
admin.site.register(AddWeight)
admin.site.register(Profile)
admin.site.register(Weight)
admin.site.register(Activities)
admin.site.register(Calculate)

