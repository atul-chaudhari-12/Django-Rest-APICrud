from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from college.models import Profile,Courses
from college.teacher.models import Teacher

class Student(models.Model):
    
    profile = models.ForeignKey(Profile)
    classrepresentative = models.BooleanField(default=False)
    studing_in = models.ForeignKey(Courses)
    mentor = models.ForeignKey(Teacher)