from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from .views import *
from rest_framework_simplejwt.views import *

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login-custom/', LoginView.as_view(), name='login-custom'),
    path('update-user/',UpdateUserView.as_view(),name='update-user'),
    path('change-password/', ChangePasswordView.as_view(),name='change-password'),    
    path('logout/',  TokenBlacklistView.as_view(), name='logout'),
    
    path('forgot-password/', ResetPasswordEmailRequest.as_view(),name='user-forgot-password'),
    path('check-token-to-reset-password/<id>/<token>/',PasswordTokenCheckAPI.as_view(),name='password-reset'),
    path('reset-password/',SetNewPasswordAPI.as_view(),name='password-reset-complete'),

    #path('themes/', ThemeAPIView.as_view(), name='theme-list-add'),
    path('theme-detail/', ThemeDetailAPIView.as_view(), name='theme-detail-list-add'),
    path('theme-detail/<user_id>', ThemeDetailUpdateAPIView.as_view(), name='theme-detail-update'),

]
# urlpatterns = [
#     path('image/', ImageView.as_view(), name='image-list-add'),
# ]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)