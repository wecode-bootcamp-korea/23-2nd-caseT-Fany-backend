# Generated by Django 3.2.6 on 2021-08-24 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_rename_nane_color_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customimage',
            name='image',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='image_file',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description_image',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='main_image',
            field=models.URLField(null=True),
        ),
    ]
