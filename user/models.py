from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.

class User(AbstractUser):
    is_marketer = models.BooleanField(default=False, verbose_name='Marketer')
    is_accountant = models.BooleanField(default=False, verbose_name='Accountant')
    is_admin = models.BooleanField(default=False, verbose_name='Admin')
    contact = models.CharField(max_length = 250, null = True, blank = True)
    no_of_wins = models.IntegerField(blank = True, null = True)
    rating = models.IntegerField(blank = True, null = True)
    no_of_followup = models.IntegerField(blank = True, null = True)
    
    profile_picture = models.ImageField(
        upload_to='profile_pics', blank=True, null=True)

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return str(self.first_name) or ''

# Signal to create a token for the user upon user creation
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserProfile(models.Model):
    # Create a one-to-one relationship with the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length = 250)
    

    def __str__(self):
        return self.user.username

