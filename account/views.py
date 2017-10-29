__author__ = 'Nathaniel'

import datetime, operator
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import *
from django.contrib.auth.decorators import user_passes_test

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authentication import *

from commonutils import from_querydict_to_dict,format_dict
from account.utils import *
from account.models import *
from account.serializers import *


@csrf_exempt
@api_view(['POST'])
@authentication_classes((BasicAuthentication,))
def login(request):
    # generate a new auth token
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
    except Token.DoesNotExist:
        '''nothing'''
    token = Token.objects.create(user=request.user)
    token.save()
    # check whether it's an organization
    credit=0
    if (hasattr(request.user,"userprofile")):
        credit = request.user.userprofile.credit
    is_organization=True if (hasattr(request.user,"organizerprofile")) else False

    # successful response
    data = {
        "token": token.key,
        "is_org":is_organization,
        "credit":credit
    }
    return Response(data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def create_account(request):
    # get data from request
    username = request.data['username']
    password = request.data['password']

    # check existing username
    if existing_user(username):
        data = {
            'message': 'The username already exists in the system'
        }
        return Response(data=data, status=status.HTTP_403_FORBIDDEN)

    # create User
    user = User.objects.create_user(username=username, password=password)
    user.save()

    # create UserProfile
    user_profile = UserProfile.objects.create(user=user, phone='', location='')
    user_profile.save()

    # create UserEmailPreference
    user_email_preference = UserEmailPreference.objects.create(user=user_profile)
    user_email_preference.save()

    # create UserStatus
    user_status = UserStatus.objects.create(user=user_profile)
    user_status.save()

    # create VerificationToken
    verification_token = VerificationToken.objects.create(user=user_profile, token=random_token_string(10))
    verification_token.save()

    # create Token
    token = Token.objects.create(user=user)
    token.save()

    # populate response data
    data = {
        'token': token.key
    }

    # successful response
    return Response(data=data)


@csrf_exempt
@api_view(['POST'])
def create_org(request):
    # get data from request
    name = request.data['name']
    username = request.data['username']
    password = request.data['password']

    # check existing username
    if existing_user(username):
        data = {
            'message': 'The username already exists in the system'
        }
        return Response(data=data, status=status.HTTP_403_FORBIDDEN)

    # create User
    user = User.objects.create_user(username=username, password=password)
    user.save()

    # create OrganizationProfile
    org_profile = OrganizerProfile.objects.create(user=user, name=name)
    org_profile.save()

    # create Token
    token = Token.objects.create(user=user)
    token.save()

    # populate response data
    data = {
        'token': token.key
    }

    # successful response
    return Response(data=data)


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def check_username(request):
    # get data from request
    username = request.data['username']

    # populate response data
    data = {
        'exists': existing_user(username)
    }

    # successful response
    return Response(data=data)


@csrf_exempt
@api_view(['POST'])
def check_token(request):
    return Response(status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def activate_account(request, token):
    # get VerificationToken
    verification_token = VerificationToken.objects.get(user__user=request.user)

    # valid token
    if token == verification_token.token:
        # update UserStatus
        user_status = UserStatus.objects.get(user_profile__user=request.user)
        user_status.is_setup = True
        user_status.save()

        # delete VerificationToken
        verification_token.delete()

        # successful response
        return Response(status=status.HTTP_200_OK)

    # if invalid token
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@csrf_exempt
@api_view(['POST'])
def change_password(request):
    # get data from request
    password = request.data['password']
    user = request.user

    # change password
    user.set_password(password)
    user.save()

    # change token
    token = Token.objects.get(user=user)
    token.delete()
    token = Token.objects.create(user=user)
    token.save()

    # successful response
    data = {
        'token': token.key
    }
    return Response(data=data)


@csrf_exempt
@api_view(['POST'])
def forget_password(request):
    # get data from request
    username = request.data['username']

    # check not existing username
    if not existing_user(username):
        return Response(status=status.HTTP_403_FORBIDDEN)

    # check too frequent action
    user_status = UserStatus.objects.get(user__user=request.user)
    if too_frequent(user_status.last_resend_password):
        return Response(status=status.HTTP_403_FORBIDDEN)

    # todo: resend password

    # successful response
    return Response(status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def set_preference(request):
    # get data from request
    tag_ids = request.data

    # check invalid tag id
    for i in tag_ids:
        try:
            EventTag.objects.get(id=i)
        except EventTag.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)

    # delete all previous UserEventPreference
    UserEventPreference.objects.filter(user__user=request.user).delete()

    # create new UserEventPreference
    user_profile = UserProfile.objects.get(user=request.user)
    for i in tag_ids:
        tag = EventTag.objects.get(id=i)
        user_event_pref = UserEventPreference.objects.create(user=user_profile, tag=tag)
        user_event_pref.save()

    # successful response
    return Response(status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def get_preference(request):
    # get user tags
    tags = UserEventPreference.objects.filter(user__user=request.user)

    # populate response data
    data = []
    for t in tags:
        data.append(t.id)

    # successful response
    return Response(data=data)


@csrf_exempt
@api_view(['GET'])
def credit_details(request):
    # get UserProfile
    user_profile = UserProfile.objects.get(user=request.user)

    # populate response data
    data = {
        'balance': user_profile.credit
    }

    # successful response
    return Response(data=data)


@csrf_exempt
@api_view(['GET'])
def credit_history(request):
    # get all UserCreditEarningHistory
    earnings = UserCreditEarningHistory.objects.filter(user__user=request.user)

    # get all EventTicketDiscount
    # todo: EventTicketDiscount not ready yet

    # populate response data
    # earnings
    data = []
    for e in earnings:
        data.append({
            'type': 'earning',
            'amount': e.amount,
            'datetime': e.datetime
        })

    # spendings
    # todo:

    # sort data by datetime desc
    data.sort(key=operator.itemgetter('datetime'), reverse=True)

    # successful response
    return Response(data=data)

class UserCreditRecordViewSet(viewsets.ModelViewSet):
    queryset = UserCreditEarningHistory.objects.all()
    serializer_class = UserCreditEarningHistorySerializer

    def get_queryset(self):
        return UserCreditEarningHistory.objects.filter(user__user=self.request.user).order_by('datetime')

    def create(self, request, *args, **kwargs):
        nonstr_field_category_dict={
            'int':['amount'],'float':[],
            'datetime':['datetime'],'boolean':[]
        }
        normalized_post_dict=from_querydict_to_dict(request.POST.copy())
        formatted_dict=format_dict(normalized_post_dict,
                                       field_category_dict=nonstr_field_category_dict)
        user_profile=request.user.userprofile
        history= UserCreditEarningHistory.objects.create(
            user=request.user.userprofile,
            datetime=formatted_dict['datetime'],
            description=formatted_dict['description'],
            amount=formatted_dict['amount']
        )
        user_profile.credit += history.amount
        user_profile.save()
        history_data=UserCreditEarningHistorySerializer(history).data
        return Response(data=history_data,status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes((AllowAny,))
def is_organization(request):
    user=request.user
    if (hasattr(user,"organizerprofile")):
        return Response(data={"answer":True},status=status.HTTP_200_OK)
    else:
        return Response(data={"answer":False},status=status.HTTP_200_OK)