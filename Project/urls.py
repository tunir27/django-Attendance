"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from login.views import logout_user
from att_app.views import ResetPasswordRequestView,PasswordResetConfirmView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('att_app.urls')),
    path('login/', include('login.urls')),
    path('signout/',logout_user, name='logout_user'),
    re_path(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    path('reset_password/',ResetPasswordRequestView.as_view(),name="reset_password")

]
