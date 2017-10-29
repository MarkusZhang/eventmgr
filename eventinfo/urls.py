from django.conf.urls import patterns, include, url
from rest_framework import routers

from views import *

router = routers.DefaultRouter()
router.register(r'category', EventCategoryViewSet)
router.register(r'local-event', LocalEventViewSet)
router.register(r'third-party-event', ThirdPartyEventViewSet)

urlpatterns = patterns('eventinfo.views',
    #url(r'event/search/',)
    url(r'^list/', EventInfoListView.as_view(),name="event_list"),
    url(r'^home/', EventHomeView.as_view(),name="event_home"),
    url(r'^task/crawl/', 'crawl_for_events',name="event_crawl"),
   url(r'^', include(router.urls)),
)