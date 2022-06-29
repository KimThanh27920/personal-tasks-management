from multiprocessing import AuthenticationError
from xml.parsers.expat import model
from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser, ThemeDetail, Themes

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import update_last_login
# from django.utils.encoding import smart_str, force_str,smart_bytes, DjangoUnicodeDecodeError
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


#register user
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    class Meta:
        model = CustomUser
        fields =['id', 'full_name','email', 'password']

        extra_kwargs = {
                        'id':{'read_only':True},
                        'password':{'write_only':True}
                        }


#login user with JWT
class LoginSerializer(TokenObtainPairSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["email"] = str(self.user.email)
        data["full_name"] = str(self.user.full_name)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

# update profile user
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','full_name']
        read_only_fields = ['id']

#send request to reset password    
class ResetPasswordEmailRequestSeriallizer(serializers.Serializer):
    email  = serializers.EmailField(min_length = 2)
    
    class Meta:
        fields =['email']

#check token and set new password
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length= 255, min_length = 2, write_only = True)
    token = serializers.CharField( min_length = 2, write_only = True)
    id = serializers.IntegerField( write_only = True)
    class Meta:
        fields = ['password', 'token', 'id']
    
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            #uidb64 = attrs.get('uidb64')
            id  = attrs.get('id')
            #id = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationError('The reset password link is invalid',401)
            user.set_password(password)
            user.save()
            return (user)
        except Exception as e :
            raise AuthenticationError('The reset password link is invalid',401)
        # return super().validate(attrs)

# serializer for change password
class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['old_password','new_password']
        write_only_fields = ['old_password','new_password']
#theme
# class ThemeSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Themes
#         fields = '__all__'

#theme of user
class ThemeDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ThemeDetail
        fields = '__all__'
#serializer for create/update theme of user
class ThemeDetailCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset= CustomUser.objects.exclude(id__in = ThemeDetail.objects.values_list('user')))
    class Meta:
        model = ThemeDetail
        fields = '__all__'