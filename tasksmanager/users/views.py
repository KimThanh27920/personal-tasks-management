
import email
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt import tokens
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str,smart_bytes, DjangoUnicodeDecodeError
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site

from .utils import Util
from .serializers import (ChangePasswordSerializer, RegisterSerializer,ResetPasswordEmailRequestSeriallizer,SetNewPasswordSerializer
                            ,LoginSerializer,UpdateUserSerializer,
                             ThemeDetailSerializer, ThemeDetailCreateSerializer)
from .models import CustomUser, ThemeDetail
# Create your views here.


#api register user
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer 
    queryset = CustomUser.objects.all()

    def perform_create(self, serializer):
        password = serializer.validated_data["password"]
        serializer.validated_data["password"] = make_password(password)
        self.user = serializer.save()
        return super().perform_create(serializer)
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        refresh = tokens.RefreshToken.for_user(self.user)
        data = response.data 
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return Response(data, status=status.HTTP_201_CREATED)


#api login with JWT
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

#api update profile user
class UpdateUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]
   
   #override to get api with current user, no lookup_url_fields
    def get_object(self):
        #queryset = self.get_queryset()
        obj = get_object_or_404(CustomUser, id=self.request.user.id)
        return obj
   
    def get_queryset(self):
        queryset = get_object_or_404(CustomUser, pk=self.request.user.id)
        return queryset
    
    #override to update profile currentuser
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

#api change password
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'message':'Old password is wrong'})
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            refresh = tokens.RefreshToken.for_user(self.object)
            res = {
                'message':'Change password successful',
                'token':{
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            }
            return Response(res, status= status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#api reset password with email
class ResetPasswordEmailRequest(GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSeriallizer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        try:
            user = CustomUser.objects.filter(email =email)
        except:
            return Response({'message':'Email do not exist'},status=status.HTTP_400_BAD_REQUEST)
        
        if  user.exists():
            user = CustomUser.objects.get(email =email)
            # uidb64 = urlsafe_base64_encode(user.id)

            token = PasswordResetTokenGenerator().make_token(user)

            #send_mail
            current_site = get_current_site(request = request).domain
            relativeLink = reverse('password-reset', kwargs={'id':user.id, 'token':token})
            absurl = 'http://'+ current_site+relativeLink+"?token="+str(token)
            email_body = 'Hi '+ user.full_name + '\n Use link below to reset your passoword \n'+absurl
            data = {
                'email_body': email_body,
                'to_email': user.email,
                'email_subject': 'Reset Passowrd'
            }

            Util.send_mail(data)
        # serializer.is_valid(raise_exception=True)
            return Response({'success':'We have sent you a link to reset your password'}, status.HTTP_200_OK)
        return Response({'message':'Email do not exist'},status=status.HTTP_400_BAD_REQUEST)


#check token to reswt password
class PasswordTokenCheckAPI(GenericAPIView):
    def get(self, request, id, token):
        try:
            #id = urlsafe_base64_decode(id)
            user = CustomUser.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response({'message':'Token is invalid'}, status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True, 'message':'Credentials Valid', 'id': id ,'token': token}, status=status.HTTP_200_OK )
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'message':'Token is invalid'}, status.HTTP_401_UNAUTHORIZED)

#reset password after check token
class SetNewPasswordAPI(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    
    def patch(self, request):
        serializer = self.serializer_class(data = request.data)

        serializer.is_valid(raise_exception=True)
        return Response({'success':True,'message':'Passwors is reset successful'}, status.HTTP_200_OK)
#create/view theme
# class ThemeAPIView(generics.ListCreateAPIView):
#     serializer_class = ThemeSerializer
#     queryset = Themes.objects.all()

#create/view theme of user
class ThemeDetailAPIView(generics.ListCreateAPIView):
    # serializer_class = ThemeDetailSerializer
    queryset = ThemeDetail.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ThemeDetailSerializer
        return ThemeDetailCreateSerializer

#update or delete theme of user
class ThemeDetailUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    #serializer_class = ThemeDetailSerializer
    queryset = ThemeDetail.objects.all()
    lookup_url_kwarg = 'user_id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ThemeDetailSerializer
        return ThemeDetailCreateSerializer

