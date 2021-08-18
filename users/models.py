from django.db import models

class User(models.Model):
    email        = models.EmailField(max_length=200)
    password     = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=45)
    address      = models.CharField(max_length=200, null=True)
    user_image   = models.CharField(max_length=500, null=True)
    nickname     = models.CharField(max_length=50, null=True)
    birthday     = models.DateField(null=True)
    kakao_number = models.CharField(max_length=500, null=True) 

    class Meta:
        db_table = 'users'