from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(OrganizerProfile)
admin.site.register(EventTag)
admin.site.register(UserEventPreference)
admin.site.register(VerificationToken)
admin.site.register(Demand)
admin.site.register(Support)
admin.site.register(UserStatus)
admin.site.register(UserCreditEarningHistory)
admin.site.register(Gift)
admin.site.register(Redemption)