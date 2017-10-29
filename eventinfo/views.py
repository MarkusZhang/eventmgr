from django.views.generic import ListView,TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from rest_framework import viewsets

from tasks import do_crawler_task

from models import ThirdPartyEvent,EventCategory,LocalEvent
from serializer import *
from filter import *

class EventCategoryViewSet(viewsets.ModelViewSet):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    filter_fields=('name',)

class LocalEventViewSet(viewsets.ModelViewSet):
    #TODO: save related fields when creating/ updating
    queryset = LocalEvent.objects.all()
    serializer_class = LocalEventSerializer
    filter_class=LocalEventFilter


class ThirdPartyEventViewSet(viewsets.ModelViewSet):
    #TODO: save related fields when creating/ updating
    queryset = ThirdPartyEvent.objects.all()
    serializer_class = ThirdPartyEventSerializer
    filter_class=ThirdPartyEventFilter


#-------------------the following are for local testing only----------------------
class EventInfoListView(ListView):
    model = ThirdPartyEvent
    template_name = "eventinfo/event_list.html"

def crawl_for_events(request):
    do_crawler_task()
    return HttpResponseRedirect(reverse("event_list"))

class EventHomeView(TemplateView):
    template_name = "eventinfo/home.html"