from users.models import User
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password

class EmailAuthBackend(BaseBackend):
    # Authenticate using an email address
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            print(password)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
