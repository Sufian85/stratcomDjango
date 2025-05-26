from django.db import models
from django.contrib.auth.models import User
import uuid
from django.dispatch import receiver
import os
from django.db.models.signals import pre_save, post_delete

# Create your models here.
class Product(models.Model):
    owner = models.ForeignKey(User, 
                on_delete=models.CASCADE)
    name = models.CharField(max_length=300, 
                default="")
    qty = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    description = models.TextField()
    image = models.ImageField(upload_to="products", 
                default="products/img.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.price}"
    
    def save(self, *args, **kwargs):
        try:
            old_file = Product.objects.get(pk=self.pk).image
        except Product.DoesNotExist:
            return False
        else:
            new_file = self.image
            if not old_file == new_file:
                try:
                    if os.path.isfile(old_file.path):
                        os.remove(old_file.path)
                except Exception:
                    return False
        finally:
            return super().save(*args, **kwargs)
        
@receiver(post_delete, sender=Product)
def delete_image(sender, instance, *args, **kwargs):
    try:
        instance.image.delete(save=False)
    except:
        pass
    
class Order(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"order {self.pk} - {self.owner.get_full_name()}"
    
class OrderItems(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    amount = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.qty} "