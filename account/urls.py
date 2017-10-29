__author__ = 'Nathaniel'
from django.conf.urls import patterns, include, url
from rest_framework import routers

from account.views import *

router = routers.DefaultRouter()
router.register(r'credit-record', UserCreditRecordViewSet)

urlpatterns = [
    url(r'^/create/user/$', create_account),
    url(r'^/create/org/$', create_org),
    url(r'^check/username/$', check_username),
    url(r'^check/token/$', check_token),
    url(r'^activate/(<token>)', activate_account),
    url(r'^password/change/', change_password),
    url(r'^password/forget/', forget_password),
    url(r'^preference/set/', set_preference),
    url(r'^preference/get/', get_preference),
    url(r'^credit/detail/', credit_details),
    url(r'^credit/history/', credit_history),
    url(r'^login/', login),
    url(r'^is-organization/', is_organization),
    url(r'^', include(router.urls))

]