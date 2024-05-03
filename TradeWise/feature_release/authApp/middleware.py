import uuid
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.request import Request
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import get_user
from authApp.models import UserLogoutHistory
from django.http import JsonResponse


class AuthMiddleware:

    def get_user_jwt(self, request):
        try:
            user = get_user(request)
            if user.is_authenticated:
                return user, None
            try:
                user_jwt = JWTAuthentication().authenticate(Request(request))
                if user_jwt is not None:
                    return user_jwt[0], user_jwt[1]
            except:
                pass
            return user, None
        except:
            return None, None

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            request_meta = request.META
            if 'HTTP_REQUEST_ID' in request_meta and request_meta['HTTP_REQUEST_ID']:
                request_id = request_meta['HTTP_REQUEST_ID']
            else:
                request_id = str(uuid.uuid4())
            user_obj, user_jwt = self.get_user_jwt(request)
            request.user = SimpleLazyObject(lambda: user_obj)
            request.user_role = None
            request.request_id = request_id
            if not request.user.is_authenticated:
                return self.get_response(request)
            if self.is_user_logged_out(user_jwt):
                return JsonResponse({
                    "message": "You have been logged out. Please login again.", "status": 0
                }, status=401)
            if user_jwt:
                request.user_role = user_jwt.payload.get('user_role')
            request.GET = request.GET.copy()
            request.payloadDict = {
                'user_id': user_obj.id,
                'is_active': user_obj.is_active,
                'userEmail': user_obj.email,
            }
            response = self.get_response(request)
            return response
        except:
            return None

    def is_user_logged_out(self, user_jwt):
        try:
            if user_jwt:
                jwt_created_time = user_jwt.payload.get('iat')
                user_id = user_jwt.payload.get('user_id')
                try:
                    last_logout = UserLogoutHistory.get_last_logout_time(user_id=user_id)
                except:
                    last_logout = None
                if last_logout and (not jwt_created_time or jwt_created_time <= last_logout):
                    return True
        except:
            pass
        return False
