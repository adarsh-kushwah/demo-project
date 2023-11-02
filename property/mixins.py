from django.core.exceptions import PermissionDenied


class OwnerLoginMixin:
    """
    mixing to logout authenticated user
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        return super().dispatch(request, *args, **kwargs)


class UserAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        # Get the user ID from the URL parameters
        url_user_id = kwargs.get("id")

        # Check if the URL's user ID matches the logged-in user's ID
        if str(request.user.id) != url_user_id:
            raise PermissionDenied("You do not have permission to access this.")

        return super().dispatch(request, *args, **kwargs)
