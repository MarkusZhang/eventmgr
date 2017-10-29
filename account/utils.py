__author__ = 'Nathaniel'

import random, string, datetime

from django.contrib.auth.models import User
from django.utils import timezone


# check if a username exists in the system
def existing_user(username):
    try:
        User.objects.get(username=username)
        return True
    except User.DoesNotExist:
        return False


# get a random token string consisting only upper case letters and numbers
# the default length is 6
def random_token_string(length=6):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))


# get timezone-aware object representing now
def timezone_aware_now():
    return make_aware(datetime.datetime.now())


# make aware a datetime according to the local timezone
def make_aware(dt):
    return timezone.make_aware(dt, timezone.get_default_timezone())


# check if the last time of some action was within 30 seconds before now
def too_frequent(last_time):
    now = timezone_aware_now()
    one_min_ago = now - datetime.timedelta(seconds=30)
    if last_time > one_min_ago:
        return True
    else:
        return False

