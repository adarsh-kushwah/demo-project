from django.contrib.auth import logout


class LogoutIfAuthenticatedMixin:
    """
    mixing to logout authenticated user
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return super().dispatch(request, *args, **kwargs)