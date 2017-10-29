from django.db import models

from account.models import OrganizerProfile
from constants import NA,LOCAL_EVENT_IMAGE_DIR,THIRD_PARTY_EVENT_IMAGE_DIR
from location import get_lng_lat
from categorizer import auto_select_event_category

class EventLocation(models.Model):
    """
        * for storing location of event venue *
    """
    longitude=models.DecimalField(max_digits=20,decimal_places=5)
    latitude=models.DecimalField(max_digits=20,decimal_places=5)
    address_str=models.TextField()

    def __unicode__(self):
        return self.address_str + "("+str(self.longitude)+","+str(self.latitude) + ")"

class EventCategory(models.Model):
    name=models.CharField(max_length=250,unique=True)
    keywords=models.TextField() # different keywords should be split by new line

    def __unicode__(self):
        return self.name

class LocalEvent(models.Model):
    title=models.CharField(max_length=250,default=NA)
    description=models.TextField()
    location=models.ForeignKey(EventLocation)
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    fee=models.DecimalField(max_digits=20,decimal_places=2)
    organizer=models.CharField(max_length=250) # for displaying purpose only
    number_of_participants=models.IntegerField(default=0)
    max_number_of_participants=models.IntegerField()
    category=models.ForeignKey(EventCategory,null=True,on_delete=models.SET_NULL)
    picture=models.FileField(upload_to=LOCAL_EVENT_IMAGE_DIR,null=True,blank=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        # categorize event
        if (not self.category):
            category=auto_select_event_category(event_info=self.__dict__,categories=EventCategory.objects.all())
            self.category=category
        super(LocalEvent, self).save(*args, **kwargs)


class ThirdPartyEvent(models.Model):
    """
        * for storing events crawled from other websites
    """
    title=models.CharField(max_length=200,default=NA)
    description=models.TextField(null=True)
    venue=models.TextField()
    location=models.ForeignKey(EventLocation,null=True)
    organizer=models.CharField(max_length=250,default=NA)
    link=models.TextField(default="#")
    fee=models.DecimalField(max_digits=10,decimal_places=2,default=0.0,null=True)
    time=models.CharField(max_length=250,default=NA)
    category=models.ForeignKey(EventCategory,null=True,on_delete=models.SET_NULL)
    picture=models.FileField(upload_to=THIRD_PARTY_EVENT_IMAGE_DIR,null=True,blank=True)


    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']

    def save(self, *args, **kwargs):
        # save exact location if the venue can be recognized by google map api
        if (self.venue != NA):
            can_find,lng,lat=get_lng_lat(self.venue)
            if (can_find):
                e_location=EventLocation.objects.create(
                    address_str=self.venue,
                    longitude=float(lng),
                    latitude=float(lat)
                )
                self.location=e_location
        # categorize event
        category=auto_select_event_category(event_info=self.__dict__,categories=EventCategory.objects.all())
        self.category=category
        super(ThirdPartyEvent, self).save(*args, **kwargs)
