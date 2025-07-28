from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import ManagerProfile

class ManagerAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                # Check if user has a manager profile and is active
                if hasattr(user, 'managerprofile'):
                    if user.managerprofile.is_active:
                        return user
                    else:
                        return None  # Manager is inactive
                else:
                    # User exists but no manager profile - allow login (could be admin)
                    return user
        except ObjectDoesNotExist:
            return None
        
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None 