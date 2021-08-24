from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'categories'

class SubCategory(models.Model):
    option   = models.CharField(max_length=50)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'sub_categories'

class DetailCategory(models.Model):
    detail       = models.CharField(max_length=50)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'detail_categories'

class Product(models.Model):
    name              = models.CharField(max_length=200)
    price             = models.DecimalField(max_digits=10, decimal_places=2)
    create_at         = models.DateTimeField(auto_now_add=True)
    description_image = models.URLField(null=True)
    detail_category   = models.ForeignKey('DetailCategory', on_delete=models.SET_NULL, null=True)
    main_image        = models.URLField(null=True)

    class Meta:
        db_table = 'products'

class ProductOption(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size    = models.ForeignKey('Size', on_delete=models.CASCADE)
    color   = models.ForeignKey('Color', on_delete=models.CASCADE)
    stock   = models.PositiveIntegerField()
    sales   = models.PositiveIntegerField()

    class Meta:
        db_table = 'product_option'

class Size(models.Model):
    select_size = models.CharField(max_length=30)

    class Meta:
        db_table = 'sizes'

class Color(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'colors'

class Image(models.Model):
    image_file = models.URLField(null=True)
    product    = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'images'

class CustomProduct(models.Model):
    user         = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product      = models.ForeignKey('Product', on_delete=models.CASCADE)
    font_color   = models.ForeignKey('FontColor', on_delete=models.SET_NULL, null=True)
    font_style   = models.ForeignKey('FontStyle', on_delete=models.SET_NULL, null=True)
    custom_image = models.ForeignKey('CustomImage', on_delete=models.SET_NULL, null=True)
    custom_text  = models.CharField(max_length=20)
    coordinate_x = models.CharField(max_length=20)
    coordinate_y = models.CharField(max_length=20) 

    class Meta:
        db_table = 'custom_products'

class FontColor(models.Model):
    color = models.CharField(max_length=30)

    class Meta:
        db_table = 'font_colors'

class FontStyle(models.Model):
    style = models.CharField(max_length=30)

    class Meta:
        db_table = 'font_styles'

class CustomImage(models.Model):
    image = models.URLField(null=True)

    class Meta:
        db_table = 'custom_images'