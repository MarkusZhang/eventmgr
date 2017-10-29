from datetime import datetime
from threading import Thread

from django.db import transaction
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from test_crawler.settings import EMAIL_HOST_USER,SEND_EMAIL_UPON_REGISTRATION
from commonutils import from_querydict_to_dict,format_dict,convert_str_to_datetime
from eventinfo import save_local_event_from_dict,get_event_or_none
from eventinfo.models import LocalEvent
from account.api import add_user_credit_earning

from models import EventOrganization,EventRegistration,EventFeedback
from serializers import *
from filters import *

class CreateEvent(APIView):

    @method_decorator(transaction.atomic)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateEvent,self).dispatch(request,*args,**kwargs)

    def post(self,request):
        # TODO: check whether the current user is an organizer

        try:
            if (not "is_payment_refundable" in request.data.keys()):
                request.data["is_payment_refundable"]=False
            serializer=CreateEventSerializer(request.data)
            data=serializer.data
            data['organizer']='some organizer'
            data['start_time']=convert_str_to_datetime(request.data['start_time'])
            data['end_time']=convert_str_to_datetime(request.data['end_time'])
            local_event=save_local_event_from_dict(data)
            # create an eventorganization object
            org=EventOrganization()
            org.__dict__.update(data)
            org.organizer=request.user
            org.event=local_event
            org.time_stamp=datetime.now()
            org.save()
            # return status, msg
            return Response({'successful':True,'msg':'Event ' + str(local_event) + " is created!"},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'successful':False,'msg':'Error occurred in creating new event'},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_my_hosted_events(request):
    orgs=EventOrganization.objects.filter(organizer=request.user)
    reply_list=[HostedEventSerializer(org).data for org in orgs]
    return Response(data=reply_list,status=status.HTTP_200_OK)

@api_view(['GET'])
def delete_hosted_event(request,object_id):
    org=get_object_or_404(EventOrganization,event__id=object_id)
    org.delete()
    return Response(data={},status=status.HTTP_200_OK)

@api_view(['GET'])
def get_registration_info(request,object_id):
    registrations=EventRegistration.objects.filter(event_organization__event__id=object_id)
    reply_list=[EventHistorySerializer(reg).data for reg in registrations]
    return Response(data=reply_list,status=status.HTTP_200_OK)

class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer

    def get_queryset(self):
        return EventRegistration.objects.filter(participant=self.request.user)

    def create(self, request, *args, **kwargs):
        event_id=int(request.data["event_id"])
        event_org=EventOrganization.objects.get(event__id=event_id)
        # validate create-registration request
        if (EventRegistration.objects.filter(participant=request.user,event_organization=event_org)):
            return Response({"success":False,"msg":"You have already registered for this event"},status=status.HTTP_400_BAD_REQUEST)
        # create registration
        request.data['event_organization']=event_org.id
        request.data['participant']=request.user.id
        request.data['time_stamp']=datetime.now()
        # update number of participants
        event_org.event.number_of_participants =event_org.event.number_of_participants+1
        event_org.event.save()
        # add credit points for the user
        event=LocalEvent.objects.get(id=event_id)
        add_user_credit_earning(user=request.user,description="Registered for event: " + event.title,amount=10)
        # send email to notify organizer
        if (SEND_EMAIL_UPON_REGISTRATION):
            email_content= request.user.username + "has registered for your event: " + event.title
            email_title= request.user.username + " registered for your event"
            email_host = EMAIL_HOST_USER
            mailing_list=[event_org.organizer.email]
            thread = Thread(target = send_mail, args = (email_title,email_content,email_host,mailing_list ))
            thread.start()
        return super(EventRegistrationViewSet,self).create(request,*args,**kwargs)

class EventFeedbackViewSet(viewsets.ModelViewSet):
    queryset = EventFeedback.objects.all()
    serializer_class = EventFeedbackSerializer
    filter_class= EventFeedbackFilter

    def get_queryset(self):
        if (self.request.user.is_staff):
            return EventFeedback.objects.all()
        else:
            return EventFeedback.objects.filter(event_registration__participant=self.request.user)

    def create(self, request, *args, **kwargs):
        event_id=self.request.data['event_id']
        registration=EventRegistration.objects.get(event_organization__event__id=event_id,participant=request.user)
        request.data['event_registration']=registration.id
        # validate create-feedback request
        if (EventFeedback.objects.filter(event_registration=registration)):
            return Response({"success":False,"msg":"You have already created feedback"},status=status.HTTP_400_BAD_REQUEST)
        # create feedback
        request.data['time_stamp']=datetime.now()
        return super(EventFeedbackViewSet,self).create(request,*args,**kwargs)

class EventHistoryViewSet(viewsets.ModelViewSet):
    """
    For viewing history only
    """
    serializer_class = EventHistorySerializer
    queryset=EventRegistration.objects.all()
    http_method_names = ['get']
    filter_class=EventHistoryFilter

    def get_queryset(self):
        user = self.request.user
        return EventRegistration.objects.filter(participant=user)
