
from django.contrib import admin
from django.urls import path,include
# urls.py
from django.conf import settings
from django.conf.urls.static import static
from .views import CategoryAPIView, ProductImageAPIView, ProductSpecificationsAPIView, ProductsAPIView, SpecificationAPIView, UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,SendpasswordResetEmailView,UserPasswordResetView

urlpatterns = [
   
    path('users/register/',UserRegistrationView.as_view(),name='register'),
    path('users/login/',UserLoginView.as_view(),name='login'),
    path('users/profile/',UserProfileView.as_view(),name='profile'),
    path('users/changepassword/',UserChangePasswordView.as_view(),name='changepassword'),

    path('users/sent-reset-password-email/',SendpasswordResetEmailView.as_view(),name='sent-reset-password-email'),
    path('users/reset-password/<uid>/<token>',UserPasswordResetView.as_view(),name='reset-password'),

    path('product/categories/', CategoryAPIView.as_view(), name='category-list'),
    path('product/specifications/', SpecificationAPIView.as_view(), name='specification-list'),
    path('product/productimages/', ProductImageAPIView.as_view(), name='productimage-list'),
    path('product/products/', ProductsAPIView.as_view(), name='products-list'),
    path('product/productspecifications/', ProductSpecificationsAPIView.as_view(), name='productspecifications-list'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)