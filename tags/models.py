from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.
class TaggedItemManager(models.Manager):
  def get_tags_for(self,obj_type,obj_id):
    # // //obj_type is the type of the object that is being tagged.
    # // //obj_id is the ID of the object that is being tagged.
    # // //The get_tags_for() method returns a list of tags that are applied to the object.
    # // //The first line of the method gets the ContentType object for the object type and the object ID.
    # // //The second line of the method gets all the TaggedItem objects that are related to the object.
    # // //The third line of the method gets the tags for the object.
    # // //The fourth line of the method returns the tags.
    content_type=ContentType.objects.get_for_model(obj_type)
    return TaggedItem.objects\
    .select_related("tag")\
    .filter(
      content_type=content_type,
      object_id=obj_id
    )

class Tag(models.Model):
  label=models.CharField(max_length=255)

  def __str__(self) -> str:
    return self.label

class TaggedItem(models.Model):
  # what tag is  applied to what product
  tag=models.ForeignKey(Tag,on_delete=models.CASCADE)
  # Type(product,video,article) and 
  #id of the object
  content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
  # //content_type is a ForeignKey to the ContentType model. This model is used to store metadata about all the models in the project. It has three fields: app_label, model, and name. The first two are used to identify the model, and the third is a human-readable name.
  # //ContentType is a generic relationship. It allows a model to be related to any other model via a foreign key. It is used when you want to write code that can work with any model, rather than just one.
  object_id=models.PositiveIntegerField()
  # // //object_id is the ID of the object that is being tagged.
  content_object=GenericForeignKey()
  objects=TaggedItemManager()
  # // //content_object is a generic foreign key to the object that is being tagged.