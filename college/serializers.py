"""
    @Author : Atul Chaudhari
    @created : 23rd Nov. 2017

"""


from rest_framework import serializers
# from rest_framework.fields import warnings
from rest_framework.authtoken.models import Token
from django.forms import widgets
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from college.models import Profile

class SignInSerializer(serializers.Serializer):

    """
    @Purpose: To handle validations and populate sign in details.
    @Methods Supported: Get & Post.
    @Author : Atul Chaudhari
    """
    identification = serializers.EmailField(max_length=100)
    password = serializers.CharField()
    type = serializers.CharField()

    def validate(self, attrs):
        """
        Purpose: To validate signin serializers.
        :param self: Context Object
        :param attrs: Dictionary containing the key as field name & it's value
        :param source: Field name
        Constraints:
        User account should be present and should be active.
        :returns: attrs in case of valid inputs else error message
        """
        username = User.objects.get(email=attrs.get('identification')).username
        user = authenticate(username=username,password=attrs.get('password'))
        user_group_name = user.groups.all().first().name.capitalize()
        user_input_type = attrs.get('type').capitalize()
        
        if user_input_type != user_group_name:
            user = None        
        if user is not None:
            # 1st IF Cond. for 1st time Login after registration.
            self.instance = user
        else:
            error = _('invalid credentials')
            raise serializers.ValidationError(error)

        return attrs
    
class UserDetailsSerializer(serializers.Serializer):
    
    user_name = serializers.SerializerMethodField('get_name')
    useraddress = serializers.SerializerMethodField('get_address')
    userdesignation = serializers.SerializerMethodField('get_designation')
    usereducation = serializers.SerializerMethodField('get_education')
    usergroup = serializers.SerializerMethodField('get_group')
    user_profile_pic1 = serializers.SerializerMethodField('get_profile_pic_func')
    userprofile_id = serializers.SerializerMethodField('get_profile_id')
    userabout_info = serializers.SerializerMethodField('get_about_info')
    useremail_id = serializers.SerializerMethodField('get_email_id')
    usersusername = serializers.SerializerMethodField('get_username')
    user_addressdict = serializers.SerializerMethodField('get_useraddressdict')
#     userprofileimage = serializers.SerializerMethodField('get_profile_image')
#     

    def get_useraddressdict(self,obj):
        try:
            add_dict = {'address1':obj.address.address1,'address2':obj.address.address2, 'city':obj.address.city}
            return add_dict
        except Exception as ex:
            return {'address1':None,'address2':None, 'city':None}
    def get_username(self,obj):
        try:
            return obj.user.username
        except:
            return None
    
    def get_email_id(self,obj):
        try:
            return obj.user.email
        except:
            return None
        
    def get_about_info(self,obj):
        try:
            return obj.aboutme
        except:
            return None

    def get_profile_id(self,obj):
        try:
            return obj.id
        except:
            return None
    def get_profile_pic_func(self,obj):
        try:
            return "/static/"+obj.profile_pic.thumbnail.split('static')[-1]
        except:
            return "/static/images/biz-man.png"
    
    def get_name(self,obj):
        try:
            return obj.user.get_full_name()
        except:
            return None
    
    def get_address(self,obj):
        try:
            return obj.address.address1 +", "+obj.address.address2+", "+obj.address.city+", "+obj.address.district
        except:
            return None
    
    def get_designation(self,obj):
        try:
            return obj.designation
        except:
            return None
    
    def get_education(self,obj):
        try:
            return obj.education
        except:
            return None
    
    def get_group(self,obj):
        try:
            return obj.user.groups.all().last().name
        except:
            return None
    
    class Meta:
        model = Profile
        feilds = ('user_name','useraddress','userdesignation','usereducation','usergroup','userprofile_id','user_profile_pic1',
                  'userabout_info','useremail_id','usersusername','user_addressdict')