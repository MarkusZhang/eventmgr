from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=20)
    location = models.TextField(null=True)
    credit = models.IntegerField(default=0)

    def __unicode__(self):
        return "profile of "+self.user.username

class OrganizerProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class EventTag(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class UserEventPreference(models.Model):
    user = models.ForeignKey(UserProfile)
    tag = models.ForeignKey(EventTag)

    class Meta:
        unique_together = ('user', 'tag')

    def __unicode__(self):
        return self.user.username + ":" + self.tag.name

class UserEmailPreference(models.Model):
    weekly_newsletter = models.BooleanField(default=True)
    one_day_notification = models.BooleanField(default=True)
    three_hour_notification = models.BooleanField(default=True)
    new_feature = models.BooleanField(default=True)


class VerificationToken(models.Model):
    user = models.OneToOneField(UserProfile)
    token = models.CharField(max_length=10)

    def __unicode__(self):
        return self.token

class Demand(models.Model):
    user = models.ForeignKey(UserProfile)
    title = models.TextField()
    description = models.TextField()

    def __unicode__(self):
        return self.title

class Support(models.Model):
    user = models.ForeignKey(UserProfile)
    demand = models.ForeignKey(Demand)
    comment = models.TextField()

    class Meta:
        unique_together = ('user', 'demand')

    def __unicode__(self):
        return "for demand : "+self.demand.title

class UserStatus(models.Model):
    user = models.OneToOneField(UserProfile)
    is_verified = models.BooleanField(default=False)
    is_setup = models.BooleanField(default=False)
    last_resend_password = models.DateTimeField(auto_now_add=True)
    last_resend_token = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "status for " + self.user.user.username

class UserCreditEarningHistory(models.Model):
    user = models.ForeignKey(UserProfile)
    description = models.CharField(max_length=100)
    amount = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "credit history of " + self.user.user.username

class Gift(models.Model):
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()

    def __unicode__(self):
        return self.description

class Redemption(models.Model):
    user = models.ForeignKey(UserProfile)
    gift = models.ForeignKey(Gift)
    datetime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "redemption of " + self.gift.description

class EventTickerDiscount(models.Model):
    # todo: payment model not ready yet
    ''
