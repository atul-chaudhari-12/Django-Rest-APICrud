from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from college.models import Profile,Courses

class Teacher(models.Model):
    
    profile = models.ForeignKey(Profile)
    classteacher = models.ForeignKey(Courses)
    