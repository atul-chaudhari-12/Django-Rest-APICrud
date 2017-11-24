# -*- coding: utf-8 -*-
"""
 @Author: Atul Chaudhari
 @Purpose : College app view
 @dated : 23rd Nov 2017 
"""
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from college.models import Profile,Media,Address
from rest_framework import viewsets, generics,parsers,renderers,status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.middleware.csrf import rotate_token
from django.core.urlresolvers import reverse
from college.serializers import SignInSerializer, UserDetailsSerializer
from django.contrib.sessions.models import Session
import datetime
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import UploadedFile
from college.utils import thumbnail

MAX_AGE = 180 * 24 * 60 * 60  #set in seconds
EXPIRES = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=MAX_AGE), "%a, %d-%b-%Y %H:%M:%S GMT")

def AuthMixin(fun):
    """
        @purpose : Decorator to maintain user log in
        @description: if user is not associed with request, mark a query to django session to get current active user and assign it to request.user. 
        @param: <function>
        @return: <function>
        @todo: Form a middleware for the same
    """
    def wrapper(self,request,*args,**kwargs):
        session_id = request._request.COOKIES.get('sessionid')
        token = request._request.COOKIES.get('authenticate')
        if request.user.is_anonymous():
            if session_id:
                session = Session.objects.get(session_key=session_id)
                uid = session.get_decoded().get('member_id')
                request.user = User.objects.get(pk=uid)
            elif token:
                request.user = Token.objects.get(pk=token).user
            else:
                request.user = request._request.user
        else:
            request.user = request.user
        return fun(self,request,*args, **kwargs)
    return wrapper

@csrf_exempt
def SignUpViewSet(request):
    """
        @purpose: To signup on the site
        @description: 
        @param: <email>,<password>,<name>,<mobile>
        @return: <userobj>
    """
    data = request.POST
    name = data.get('user_name',None)
    email = data.get('email',None)
    mobile = data.get('mobile',None)
    password = data.get('password',None)
    type = data.get('type','staff')
    user = User.objects.filter(email=email).exists()
    if not user:
        username=name + str(User.objects.count())
        new_user = User.objects.create_user(username,email,password)
        new_user.first_name = name 
        g,status = Group.objects.get_or_create(name=type)  
        g.user_set.add(new_user)   
        new_user.save()  
    else:
        return render_to_response('home.html')
    
    user_profile = Profile.objects.create(user=new_user,mobile=mobile,djangousergroup=type)
    request.user = new_user
    request.session['member_id']=new_user.id    
    return HttpResponseRedirect('/afterlogin')

class ObtainAuthToken(APIView):
    """
        @purpose : TO log in into the account
        @param param: <email>,<password>
        @return: loged in user
        @redirectd : afterlogin page
    
    """
    throttle_classes = ()
    authentication_classes = ()
    permission_classes = (AllowAny,)
    parser_classes = (
        parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = SignInSerializer  # AuthTokenSerializer
    model = Token
    
    def post(self, request, backend):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.instance
            rotate_token(request)
            user_logged_in.send(
                sender=user.__class__, request=request, user=user)
            token, created = Token.objects.get_or_create(user=user)
            template_name = "afterlogin"
            redirect_url = reverse('generic_view',
                kwargs={
                    "template_name": template_name}
            )
            response = Response({'token': token.key,
                                         'profileid': user.profile.id,
                                         'redirect_url': redirect_url,
                    })
            response.set_cookie('authorization', token.key, max_age=MAX_AGE, expires=EXPIRES)
            response.set_cookie('authenticate', token.key, max_age=MAX_AGE, expires=EXPIRES)
        else:
            response = Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return response


class UserDetailsViewSet(viewsets.ModelViewSet):
    """
        @purpose : get details of user
        @param param: <user>
        @return: user details
    """
    queryset = Profile.objects.all()
    serializer_class = UserDetailsSerializer
    
    @AuthMixin
    def list(self,request,*args,**kwargs):
        id = request.GET.get('id',None)
        if id:
            user = Profile.objects.get(id=id).user
        else:
            user = request.user
        serializer = UserDetailsSerializer(user.profile)
        return Response(serializer.data)
    
    @AuthMixin
    def create(self,request,*args,**kwargs):
        data = request.data
        addrs = data.get('user_addressdict')
        pic = data.get('user_profile_pic1')
        obj = Profile.objects.get(id=data.get('userprofile_id'))
        obj.aboutme = data.get('userabout_info')
        obj.education = data.get('usereducation')
        obj.first_name = data.get('user_name')
        try:
            med_obj = Media.objects.get(thumbnail=pic)
            obj.profile_pic = med_obj
        except:
            pass
        if obj.address:
            obj.address.address1 = addrs.get('address1')
            obj.address.address2 = addrs.get('address2')
            obj.address.city = addrs.get('city')
            obj.address.save()
        else:
            add_obj = Address.objects.create(address1=addrs.get('address1'),address2=addrs.get('address2'),city=addrs.get('city'))
            obj.address = add_obj
        obj.save()
        return render_to_response('afterlogin.html',{'user_id':obj.id})
        
            


class TeachersDetailsViewset(viewsets.ModelViewSet):
    
    queryset = Profile.objects.all()
    
    def list(self,request,*args,**kwargs):
        searchterm = request.GET.get('searchtearm','all')
        if searchterm == 'all':
            queryset = Profile.objects.filter(djangousergroup__in=['teacher','Teacher'])
        else:
            user_ids_list = Profile.objects.filter(djangousergroup__in=['teacher','Teacher']).values_list('user_id')
            u_ids = User.objects.filter(first_name__icontains=searchterm,id__in=user_ids_list).values_list('id',flat=True)
            queryset = Profile.objects.filter(user_id__in=u_ids)
        serializer = UserDetailsSerializer(queryset,many=True)
        return Response(serializer.data)
    
class StudentsDetailsViewset(viewsets.ModelViewSet):
    
    queryset = Profile.objects.all()
    
    def list(self,request,*args,**kwargs):
        searchterm = request.GET.get('searchtearm','all')
        if searchterm == 'all':
            queryset = Profile.objects.filter(djangousergroup__in=['student','Student','students','Students'])
        else:
            user_ids_list = Profile.objects.filter(djangousergroup__in=['student','Student','students','Students']).values_list('user_id',flat=True)
            u_ids = User.objects.filter(first_name__icontains=searchterm,id__in=user_ids_list).values_list('id',flat=True)
            queryset = Profile.objects.filter(user_id__in=u_ids)
        serializer = UserDetailsSerializer(queryset,many=True)
        return Response(serializer.data)
    
class LogoutViewSet(viewsets.ModelViewSet):
    
    queryset = Profile.objects.all()
    
    def list(self,request,*args,**kwargs):
        logout(request)
        request._request.COOKIES={}
        return Response({'status':True})
    
@csrf_exempt
def SaveMedia(request):
    
    file = request.FILES[u'file']
    file_type = file.content_type.split('/')[0]
    wrapped_file = UploadedFile(file)
    filename = wrapped_file.name
    file_size = wrapped_file.file.size
    
    fl = Media()
    fl.file = file
    fl.save()
    try:
        thumb_url = thumbnail(file, filename, fl)
        fl.thumbnail = thumb_url
        fl.save()
    except Exception as ex:
        pass
    response_dict = {'thumbanil':fl.thumbnail}
    return HttpResponse(fl.thumbnail) 


class EditProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    
    def list(self,request,*args,**kwargs):
        id = request.GET.get('id')
        return render_to_response('profileedit.html',{'user_id':id})