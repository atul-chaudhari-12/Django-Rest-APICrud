# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from college.utils import thumbnail_model


class Media(models.Model):
    
    file = models.FileField(upload_to='static/images')
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.CharField(max_length=255,null=True,blank=True)
    is_active = models.BooleanField(default=True)

class Address(models.Model):
    
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    Country = models.CharField(max_length=255,default='India')

class Courses(models.Model):
    course = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    standered = models.IntegerField()
    
class Profile(models.Model):
    user = models.OneToOneField(User)
    address = models.ForeignKey(Address,blank=True,null=True)
#     studing_in = models.ForeignKey(Courses,null=True,blank=True)
#     classrepresentative = models.ForeignKey(Courses,null=True,blank=True)
    profile_pic = models.ForeignKey(Media,null=True,blank=True)
#     classteacher = models.ForeignKey(Courses,null=True,blank=True)
    education = models.CharField(max_length=255,null=True,blank=True)
    designation = models.CharField(max_length=255,null=True,blank=True)
    mobile = models.IntegerField(max_length=10,null=True,blank=True)
    gender = models.CharField(max_length=10,null=True,blank=True)
    djangousergroup = models.CharField(max_length=255,null=True,blank=True) 
    aboutme = models.CharField(max_length=255,null=True,blank=True)
    

# class Student(models.Model):
#     
#     user = models.OneToOneField(User,required=True)
#     address = models.ForeignKey(Address,blank=True,null=True)
#     studing_in = models.ForeignKey(Courses,required=True,null=False,blank=False)
#     classrepresentative = models.ForeignKey(Courses,null=True,blank=True)
#     profile_pic = models.ForeignKey(Media,null=True,blank=True)
#     
# class Teachers(models.Model):
#     
#     user = models.OneToOneField(User,required=True)
#     address = models.ForeignKey(Address,blank=True,null=True)
#     classteacher = models.ForeignKey(Courses,null=True,blank=True)
#     education = models.CharField(max_length=255,null=True,blank=True)
#     designation = models.CharField(max_length=255,null=True,blank=True)
#     profile_pic = models.ForeignKey(Media,null=True,blank=True)
#     
# class Staff(models.Model):
#     
#     user = models.OneToOneField(User,required=True)
#     address = models.ForeignKey(Address,blank=True,null=True)
#     education = models.CharField(max_length=255,null=True,blank=True)
#     designation = models.CharField(max_length=255,null=True,blank=True)
#     profile_pic = models.ForeignKey(Media,null=True,blank=True)
    
class Subject(models.Model):
    
    name = models.CharField(max_length=255,null=False,blank=False)
    course = models.ForeignKey(Courses,null=False,blank=False)
    teacher = models.ForeignKey(Profile,null=False,blank=False)
    sylabus = models.ForeignKey(Media)
    
