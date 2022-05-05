from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.core.files import File
from urllib import request
import os


class User(AbstractUser):
    ''' model for users  '''

    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    age = models.PositiveIntegerField(default=18)
    image_url = models.URLField(default=None, null=True, blank=True)

    activation_key = models.CharField(max_length=128, blank=True, null=True)
    activation_key_expires = models.DateTimeField(auto_now=True, blank=True, null=True)

    def get_remote_image(self, image_url):
        if image_url and (self.image_url != image_url):
            self.image_url = image_url
            result = request.urlretrieve(self.image_url)
            self.image.save(
                os.path.basename(self.image_url),
                File(open(result[0], 'rb'))
            )
            self.save()

    def is_activation_key_expires(self):
        return not now() <= self.activation_key_expires + timedelta(hours=48)


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'
    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    user = models.OneToOneField(User, null=True, unique=True, db_index=True, on_delete=models.CASCADE)
    about = models.TextField(verbose_name='о себе', blank=True, null=False)
    gender = models.CharField(verbose_name='пол', choices=GENDER_CHOICES, blank=True, max_length=2)
    langs = models.TextField(verbose_name='языки', blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, created, **kwargs):
        if not created:
            instance.userprofile.save()
