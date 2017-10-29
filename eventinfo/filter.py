import django_filters

from location import is_within_distance
from models import ThirdPartyEvent,LocalEvent

#TODO: enable elastic filtering

class EventLocationFilterMixin(object):
    def search_nearby(self, queryset, value):
        distance,longitude,latitude=value.split(",")
        return [a for a in queryset if a.location and
         is_within_distance(lat1=float(latitude),lng1=float(longitude),lat2=a.location.latitude,lng2=a.location.longitude,distance=float(distance))]


class ThirdPartyEventFilter(EventLocationFilterMixin,django_filters.FilterSet):
    location_search_nearby=django_filters.MethodFilter(action='search_nearby')
    category=django_filters.CharFilter(name='category__name')

    class Meta:
        model = ThirdPartyEvent
        fields = ['title','fee','category','location_search_nearby']

class LocalEventFilter(EventLocationFilterMixin,django_filters.FilterSet):
    location_search_nearby=django_filters.MethodFilter(action='search_nearby')
    category=django_filters.CharFilter(name='category__name')

    class Meta:
        model = LocalEvent
        fields = ['title','fee','category','location_search_nearby']