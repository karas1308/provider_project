from django.contrib.auth.backends import ModelBackend

from account.models import User


class PhoneBackend(ModelBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        try:
            user = User.objects.get(phone=phone)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
