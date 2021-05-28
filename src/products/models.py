from django.db import models
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ('name',)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("Name", max_length=255)
    price = models.DecimalField("Price", max_digits=10, decimal_places=2, max_length=255)
    description = models.TextField("Description")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'
