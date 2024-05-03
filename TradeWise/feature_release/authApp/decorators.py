from django.http import JsonResponse
from rest_framework import status


def staff_internal_login_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if not user.id or (not user.is_staff and not user.is_superuser):
            return JsonResponse({'message': 'You are not autherized for the same.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return function(request, *args, **kw)

    return wrapper
