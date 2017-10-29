import django_filters

from models import EventFeedback,EventRegistration

class EventFeedbackFilter(django_filters.FilterSet):
    event_id=django_filters.CharFilter(name='event_registration__event_organization__event__id')
    user_id=django_filters.CharFilter(name='event_registration__participant__id')

    class Meta:
        model = EventFeedback
        fields = ['rating','want_again']


class EventHistoryFilter(django_filters.FilterSet):
    event_id=django_filters.CharFilter(name="event_organization__event__id")
    event_category_name=django_filters.CharFilter(name="event_organization__event__category__name")

    class Meta:
        model = EventRegistration
