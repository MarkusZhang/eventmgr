from rest_framework import serializers

from models import EventCategory,LocalEvent,ThirdPartyEvent

class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ('name','keywords')

class LocalEventSerializer(serializers.ModelSerializer):
    category=serializers.StringRelatedField(many=False)
    location=serializers.StringRelatedField(many=False)

    class Meta:
        model=LocalEvent

class ThirdPartyEventSerializer(serializers.ModelSerializer):
    category=serializers.StringRelatedField(many=False)
    location=serializers.StringRelatedField(many=False)

    class Meta:
        model=ThirdPartyEvent
        exclude=('picture',)