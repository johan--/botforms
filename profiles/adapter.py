from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Learn more: https://django-allauth.readthedocs.io/en/latest/advanced.html#custom-user-models
    """
    def is_open_for_signup(self, request):
        return False