from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import ProfileSerializer
import random
from .models import *
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from .permissions import *
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags



 
                                    ###### Authentication #####   

## Generate otp ##
def send_otp(length=6):
    characters = "0123456789"
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp


## Send email ##
def send_email(template,subject,content,recipient):
    sender = settings.EMAIL_HOST_USER
    try:
        html_content = render_to_string(template, {'content': content})
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email=sender, to=[recipient])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
        return True
    except Exception as e:
        print(e)
        return False




@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()

            otp=send_otp()
            otp_obj=OTPVerification.objects.filter(profile=user)
            if otp_obj.exists():
                otp_obj=otp_obj.first()
                otp_obj.otp=otp
                otp_obj.created_time=datetime.now()
                otp_obj.save()
            else:
                new_obj=OTPVerification.objects.create(otp=otp,profile=user,created_time=datetime.now())
                new_obj.save()

            if new_obj or otp_obj:
                template='otp.html'
                subject='Email Verification'
                content={'otp':otp}
                recipient=user.email
                email_status=send_email(template,subject,content,recipient)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    username = request.data.get('email')
    password = request.data.get('password')
    
    user = authenticate(email=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        access_token['name'] = user.first_name
        token = {
            'refresh': str(refresh),
            'access': str(access_token),
        }
        return Response(token)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


## Verify otp ##
@api_view(['POST'])
def otp_verification(request,user_id):
    if request.method=='POST':
        entered_otp=request.data.get('otp')
        profile=get_object_or_404(Profile,pk=user_id)

        current_time = timezone.now() 
        time_threshold = timedelta(minutes=5)
        otp_obj=get_object_or_404(OTPVerification,profile=profile)
        created_date_time = otp_obj.created_time

        if current_time - created_date_time < time_threshold and otp_obj.otp==entered_otp:
            profile.verify=True
            return Response({'msg':'otp verified'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':'invalid otp'},status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def resend_otp(request,user_id):
    if request.method == 'POST':
        profile=get_object_or_404(Profile,pk=user_id)
        otp=send_otp()
        otp_obj=OTPVerification.objects.filter(profile=profile)
        new_obj=None

        if otp_obj.exists():
            otp_obj=otp_obj.first()
            otp_obj.otp=otp
            otp_obj.created_time=datetime.now()
            otp_obj.save()
        else:
            new_obj=OTPVerification.objects.create(otp=otp,profile=profile,created_time=datetime.now())
            new_obj.save()

        if new_obj or otp_obj:
            template='otp.html'
            subject='Email Verification'
            content={'otp':otp}
            recipient=profile.email
            email_status=send_email(template,subject,content,recipient)

            if email_status == True:
                return Response({'msg':'otp send successfully'}, status=status.HTTP_200_OK)
        return Response({'msg':'otp sending failed '},status=status.HTTP_400_BAD_REQUEST)




                                        #### General apis ####

@api_view(['GET'])
@permission_classes([IsUser])
def get_data(request):
    if request.method=='GET':
        user=request.user
        profile=get_object_or_404(Profile,pk=user.id)
        serializer=ProfileSerializer(profile)
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response({'msg':'invalid otp'},status=status.HTTP_400_BAD_REQUEST)
    








