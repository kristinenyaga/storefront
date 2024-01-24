from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings

# Create your models here.
class LikedItem(models.Model):
  # what user likes what object
  user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
  # which product is liked
  content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
  object_id=models.PositiveIntegerField()
  content_object=GenericForeignKey()


