from django.db import models
from django.core.validators import MinValueValidator
class Promotion(models.Model):
  description=models.CharField(max_length=255)
  discount=models.FloatField()

class Collection(models.Model):
  title=models.CharField(max_length=255)
  featured_product=models.ForeignKey('Product',on_delete=models.SET_NULL,null=True,related_name='+')
  # //related_name='+' means that the relationship is not symmetrical. It is used to avoid name collisions with the reverse relationship.Django creates a reverse relationship for every ForeignKey and ManyToManyField. 
# Create your models here.
  
  def __str__(self) -> str:
    return self.title
  
  class Meta:
    ordering=['title']

  # //meta is used to specify model-specific options. In this case, we are specifying that the collections should be ordered by title by default.
  
class Product(models.Model):
  title=models.CharField(max_length=255)
  description=models.TextField(blank=True)
  unit_price=models.DecimalField(
    max_digits=6,
    decimal_places=2,
    validators=[MinValueValidator(10)]
    )  
  inventory=models.IntegerField(default=0,validators=[MinValueValidator(0)])
  last_update=models.DateTimeField(auto_now=True)
  collection= models.ForeignKey(Collection, on_delete=models.PROTECT)
  slug = models.SlugField(default='',blank=True)
  # //auto_now updates a field to the current date and time every time the object is saved, including when it is first created. It reflects the last modification time.
  # //protect means that when a collection is deleted, the product will not be deleted, but an error will be raised instead.
  promotions=models.ManyToManyField(Promotion,blank=True)

  def __str__(self) -> str:
    return self.title
  class Meta:
    ordering=['title']

class Cart(models.Model):
  created_at=models.DateTimeField(auto_now_add=True)
  # //auto_now_add sets a field to the current date and time when an object is first created. It remains the same even after updates.

class CartItem(models.Model):
  cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
  product=models.ForeignKey(Product,on_delete=models.CASCADE)
  # //on_delete=models.CASCADE means that when a product is deleted, all of its cart items will be deleted as well.
  quantity=models.PositiveSmallIntegerField()
  unitPrice=models.DecimalField(max_digits=6,decimal_places=2)

class Customer(models.Model):
  MEMBERSHIP_BRONZE='B'
  MEMBERSHIP_SILVER='S'
  MEMBERSHIP_GOLD='G'
  MEMBERSHIP_CHOICES=[
    (MEMBERSHIP_BRONZE,'Bronze'),
    (MEMBERSHIP_SILVER,'Silver'),
    (MEMBERSHIP_GOLD,'Gold')
  ]
  first_name=models.CharField(max_length=255)
  last_name=models.CharField(max_length=255)
  email=models.EmailField(unique=True)
  phone=models.CharField(max_length=255)
  birth_date=models.DateField(null=True)
  membership=models.CharField(max_length=20,choices=MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE)
  # //choices is a list of two-tuples. The first element in each tuple is the actual value to be set on the model, and the second element is the human-readable name.
  class Meta:
    db_table='store_customers'
  
  def __str__(self) -> str:
    return f'{self.first_name} {self.last_name}'


class Order(models.Model):
  placed_at=models.DateTimeField(auto_now_add=True)
  PENDING = 'P'
  COMPLETE = 'C'
  FAILED = 'F'
  PAYMENT_STATUS_CHOICES = [
    (PENDING, 'Pending'),
    (COMPLETE, 'Complete'),
    (FAILED, 'Failed'),
  ]
  payment_status=models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PENDING)
  customer=models.ForeignKey(Customer, on_delete=models.PROTECT)

class OrderItem(models.Model):
  order=models.ForeignKey(Order,on_delete=models.PROTECT)
  product=models.ForeignKey(Product,on_delete=models.PROTECT,related_name='orderitems')
  quantity=models.PositiveSmallIntegerField()
  unit_price=models.DecimalField(max_digits=6,decimal_places=2)

class Address(models.Model):
  street=models.CharField(max_length=255)
  city=models.CharField(max_length=255)
  customer=models.OneToOneField(Customer, on_delete=models.CASCADE,primary_key=True)
  




# auto_now_add sets a field to the current date and time when an object is first created. It remains the same even after updates.
# auto_now updates a field to the current date and time every time the object is saved, including when it is first created. It reflects the last modification time.