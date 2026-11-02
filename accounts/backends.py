from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class EmailAuthBackend(ModelBackend):
    """
    Authenticate users using their real email address (case-insensitive) or username.
    Allows anyone to log in with their real email and password.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get("email")
        if not username or not password:
            return None

        clean_username = username.strip()
        # Find user by email (case-insensitive) or by username
        user = User.objects.filter(email__iexact=clean_username).first()
        if not user:
            user = User.objects.filter(username__iexact=clean_username).first()

        if user and user.check_password(password):
            return user
        return None
