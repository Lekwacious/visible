from django.db.models.signals import pre_delete
import cloudinary
import cloudinary.uploader
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(pre_delete, sender=User)
def photo_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.image.public_id)