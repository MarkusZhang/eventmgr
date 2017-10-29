from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from eventinfo.models import LocalEvent

class EventOrganization(models.Model):
    event=models.OneToOneField(LocalEvent)
    organizer=models.ForeignKey(User)
    require_registration_payment=models.BooleanField(default=False)
    registration_payment_amount=models.DecimalField(max_digits=10,decimal_places=2)
    is_payment_refundable=models.BooleanField(default=False)
    time_stamp=models.DateTimeField(auto_created=True)

    def __unicode__(self):
        return self.event.title

    def delete(self, *args,**kwargs):
        self.event.delete()
        return super(EventOrganization,self).delete(*args,**kwargs)


class EventRegistration(models.Model):
    event_organization=models.ForeignKey(EventOrganization)
    participant=models.ForeignKey(User)
    special_comment=models.TextField(null=True,blank=True)
    amount_paied=models.DecimalField(max_digits=10,decimal_places=2)
    time_stamp=models.DateTimeField(auto_created=True)

    def __unicode__(self):
        return self.participant.username + " registered for: " + self.event_organization.event.title

    def get_participant_username(self):
        return self.participant.username

    def get_participant_email(self):
        return self.participant.email

    def with_feedback(self):
        return hasattr(self,"eventfeedback")

    def get_feedback_want_again(self):
        if not hasattr(self,"eventfeedback"):
            return False
        return self.eventfeedback.want_again

    def get_feedback_text(self):
        if not hasattr(self,"eventfeedback"):
            return ""
        return self.eventfeedback.comment

    def get_feedback_rating(self):
        if not hasattr(self,"eventfeedback"):
            return -1
        return self.eventfeedback.get_rating()

    def get_event(self):
        return self.event_organization.event

    def get_event_id(self):
        return self.get_event().id

    def get_event_title(self):
        return self.get_event().title

class EventAttendance(models.Model):
    event_registration=models.OneToOneField(EventRegistration)
    amount_refunded=models.DecimalField(max_digits=10,decimal_places=2)

    def __unicode__(self):
        return str(self.event_registration)

class EventFeedback(models.Model):
    RATING_CHOICE=(
        (0,'Very bad'),
        (1,'Bad'),
        (2,'Just so so'),
        (3,'Good'),
        (4,'Very good'),
    )
    event_registration=models.OneToOneField(EventRegistration)
    comment=models.TextField()
    rating=models.IntegerField(choices=RATING_CHOICE)
    want_again=models.BooleanField(default=False)
    time_stamp=models.DateTimeField(auto_now_add=True,null=True)

    def __unicode__(self):
        return str(self.event_registration)

    def get_rating(self):
        return self.RATING_CHOICE[self.rating][0]

    # def save(self,*args,**kwargs):
    #     self.time_stamp=datetime.now()
    #     super(EventFeedback,self).save(*args,**kwargs)