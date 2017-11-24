"""institute URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from .views import GetTemplate,GenericView
from college.views import SignUpViewSet
from rest_framework import routers
from college.views import UserDetailsViewSet,ObtainAuthToken,TeachersDetailsViewset,StudentsDetailsViewset,LogoutViewSet,SaveMedia,\
                        EditProfileViewSet

router = routers.DefaultRouter()

router.register(r'userdetials', UserDetailsViewSet)
router.register(r'teachersdetails',TeachersDetailsViewset)
router.register(r'studentsdetails',StudentsDetailsViewset)
router.register(r'logout',LogoutViewSet)
router.register(r'editprofile',EditProfileViewSet)



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/', GetTemplate.as_view(template_name='home.html'),name='home'),
    url(r'^signup', SignUpViewSet,name="signup"),
    url(r'^api/savemedia', SaveMedia,name="savemedia"),
    url(r'^(?P<template_name>\w+)$',GenericView.as_view(), name='generic_view'),
    url(r'^api-auth/',include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
    url(r'^api-token/login/(?P<backend>[^/]+)/$',ObtainAuthToken.as_view(),name="login"),
]
