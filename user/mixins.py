from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied


class LogoutIfAuthenticatedMixin:
    """
    mixing to logout authenticated user
    """

    def dispatch(self, request, *args, **kwargs):
        
        if request.user.is_authenticated:
            logout(request)
        return super().dispatch(request, *args, **kwargs)


class UserAccessMixin:
    """
    authenticated user can access his own profile
    """
    def dispatch(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id',None)
        
        if user_id and request.user.id != user_id:
            raise PermissionDenied("You do not have permission to access others profile.")
        
        return super().dispatch(request, *args, **kwargs)