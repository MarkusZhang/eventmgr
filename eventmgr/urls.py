from django.conf.urls import patterns, include, url
from rest_framework import routers

from views import *

router = routers.DefaultRouter()
router.register(r'registration', EventRegistrationViewSet)
router.register(r'feedback', EventFeedbackViewSet)
router.register(r'history', EventHistoryViewSet)

urlpatterns = patterns('eventmgr.views',
    #url(r'event/search/',)
    url(r'^event/create/$', CreateEvent.as_view(),name="event_list"),
    url(r'^event/view-hosted/$', get_my_hosted_events,name="get_my_hosted_events"),
    url(r'^event/delete-hosted/(?P<object_id>\d+)/$', delete_hosted_event,name="delete_hosted_event"),
    url(r'^event/get-registration-info/(?P<object_id>\d+)/$', get_registration_info,name="get_registration_info"),
    url(r'^', include(router.urls)),
)