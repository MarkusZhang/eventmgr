from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(EventOrganization)
admin.site.register(EventRegistration)
admin.site.register(EventAttendance)
admin.site.register(EventFeedback)