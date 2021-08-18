from django.db import models

class Cart(models.Model):
    user           = models.ForeignKey('users.User', on_delete=models.CASCADE)
    quantity       = models.PositiveIntegerField()
    custom_product = models.ForeignKey('products.CustomProduct', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'carts'