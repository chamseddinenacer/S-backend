from django.db import models

# Create your models here.
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  

 

class Image(models.Model):
    idimage = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.idimage



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "http://127.0.0.1:8000{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(

        # title:
        "Password Reset for {title}".format(title="Pet Adoption "),
        # message:
        email_plaintext_message,
        # from:
        "nacerchamseddine@gmail.com",
        # to:
        [reset_password_token.user.email]
    )
