from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User,
                             related_name='profile',
                             on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='user/profile_pic',
                                        blank=True)

    def __str__(self):
        return self.user


def get_details(self):
    return f"{self.first_name} : {self.username}"


User.add_to_class("__str__", get_details)
