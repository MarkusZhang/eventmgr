from rest_framework import serializers

from eventinfo.models import LocalEvent

from models import EventRegistration,EventFeedback,EventOrganization

class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration

class EventFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventFeedback

class EventHistorySerializer(serializers.ModelSerializer):
    """
    Event registration history
    """
    event_id = serializers.IntegerField(source='get_event_id', read_only=True)
    event_title=serializers.CharField(source="get_event_title",read_only=True)
    has_feedback=serializers.BooleanField(source="with_feedback")
    feedback_comment=serializers.CharField(source="get_feedback_text")
    feedback_rating=serializers.CharField(source="get_feedback_rating")
    feedback_want_again=serializers.BooleanField(source="get_feedback_want_again")
    participant_username=serializers.CharField(source="get_participant_username")
    participant_email=serializers.CharField(source="get_participant_email")

    class Meta:
        model = EventRegistration
        exclude=('event_organization','participant',)

class CreateEventSerializer(serializers.ModelSerializer):
    address_str=serializers.CharField(max_length=500)
    longitude=serializers.DecimalField(max_digits=10,decimal_places=7)
    latitude=serializers.DecimalField(max_digits=10,decimal_places=7)
    require_registration_payment=serializers.BooleanField()
    registration_payment_amount=serializers.DecimalField(max_digits=10,decimal_places=2)
    is_payment_refundable=serializers.BooleanField(default=False,required=False)

    class Meta:
        model = LocalEvent
        exclude = ('location','organizer','category','picture','start_time','end_time',)

class HostedEventSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="event.title")
    description = serializers.CharField(source="event.description")
    address=serializers.CharField(source="event.location.address_str")
    start_time=serializers.DateTimeField(source="event.start_time")
    end_time=serializers.DateTimeField(source="event.end_time")
    event_id=serializers.IntegerField(source="event.id")

    class Meta:
        model = EventOrganization
        fields = ['require_registration_payment','registration_payment_amount','is_payment_refundable',
                  "title","description","address","start_time","end_time",'event_id']