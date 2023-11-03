from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from property.models import Property


class OwnerLoginMixin:
    """
    mixing to logout authenticated user
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        return super().dispatch(request, *args, **kwargs)


class ProperetyAccessMixin:

    """
    permission mixin :- Only logged in owner can update his own property
    """

    def dispatch(self, request, *args, **kwargs):
        property_id = kwargs.get("pk",None)

        if property_id:
            property = get_object_or_404(Property, pk=property_id)

            if property.owner.id != request.user.id:
                raise PermissionDenied("You do not have permission to access others property.")
        
        return super().dispatch(request, *args, **kwargs)
