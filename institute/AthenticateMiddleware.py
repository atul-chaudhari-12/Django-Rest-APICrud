# from django.contrib.auth.models import User
# from django.contrib.sessions.models import Session
# 
# class Authenticate(object):
#     
#     def __init__(self, get_response):
#         self.get_response = get_response
#     
#     def process_request(self,request):
#         session_id = request._request.COOKIES.get('sessionid')
#         if request.user.is_anonymous():
#             if session_id:
#                 session = Session.objects.get(session_key=session_id)
#                 uid = session.get_decoded().get('_auth_user_id')
#                 request.user = User.objects.get(pk=uid)
#             else:
#                 request.user = request.request.user
#         else:
#             request.user = request.user
#         return request