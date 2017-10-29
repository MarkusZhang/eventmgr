from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(ThirdPartyEvent)
admin.site.register(LocalEvent)
admin.site.register(EventCategory)
admin.site.register(EventLocation)