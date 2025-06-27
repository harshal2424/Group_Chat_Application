from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import get_user_model
from django.apps import apps


#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
 #   if created:
  #      Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    Profile = apps.get_model('myapp', 'Profile')  # Dynamically resolve the Profile model
    instance.profile.save()

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        from .models import Profile  # Import inside the function to avoid circular import
        Profile.objects.create(user=instance)


