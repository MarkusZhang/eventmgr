from django.contrib import admin
from .models import Site,MatchingRule,AttributePairs
# Register your models here.
admin.site.register(Site)
admin.site.register(MatchingRule)
admin.site.register(AttributePairs)