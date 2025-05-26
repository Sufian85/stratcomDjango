from django.contrib.auth.models import User
from django.db import models
import os
from django.dispatch import receiver

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller')
    ]
    GENDER_TYPES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Others", "Others"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    gender = models.TextField(max_length=10, choices=GENDER_TYPES, default="Male")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=15, blank=True, null=True)
    bio_data = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="profile_pics/", blank=True, null=True, default="profile_pics/default.png")

    def __str__(self):
        return self.user.get_full_name()
    
# Signal to delete image files when a profile is deleted
@receiver(models.signals.post_delete, sender=UserProfile)
def delete_user_profile_image(sender, instance, **kwargs):
    if instance.image:   
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)