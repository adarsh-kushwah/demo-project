class OwnerLoginMixin:
    """
    mixing to logout authenticated user
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        return super().dispatch(request, *args, **kwargs)