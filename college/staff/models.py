from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from college.models import Profile,Courses

class Staff(models.Model):
    
    profile = models.ForeignKey(Profile)
    designation = models.CharField(max_length=128,null=True,blank=True)