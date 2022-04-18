from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.conf import settings


# Create your models here.

class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=255)
    IGL_Username = models.CharField(max_length=255, null=True, blank=True)
    is_varified = models.BooleanField(default=False)
    Terms_and_condition_agreement = models.BooleanField(default=True)
    code_of_conduct_agreement = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    email_token = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)
    forget_password = models.CharField(max_length=255, null=True, blank=True)
    old_password = models.CharField(max_length=255, null=True, blank=True)
    new_password = models.CharField(max_length=255, null=True, blank=True)
    last_login_time = models.DateTimeField(null=True, blank=True)
    last_logout_time = models.DateTimeField(null=True, blank=True)
    profile_image = models.ImageField(default='default-avatar.png', upload_to='users/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'),
                                                   reset_password_token.key)
    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )
