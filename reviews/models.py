from django.db import models

class Review(models.Model):
    text      = models.CharField(max_length=500, null=True)
    score     = models.PositiveIntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, null=True)
<<<<<<< HEAD
    image     = models.ImageField(upload_to='images/', blank=True, null=True)
=======
    image     = models.CharField(max_length=500)
>>>>>>> 0ea6823 (EDIT: model작성)
    product   = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    user      = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'reviews'