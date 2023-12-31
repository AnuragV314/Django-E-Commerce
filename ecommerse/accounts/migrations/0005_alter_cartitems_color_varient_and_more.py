# Generated by Django 4.2.6 on 2023-12-17 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_coupon'),
        ('accounts', '0004_cart_cartitems'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitems',
            name='color_varient',
            field=models.ManyToManyField(null=True, to='products.colorvarient'),
        ),
        migrations.AlterField(
            model_name='cartitems',
            name='size_varient',
            field=models.ManyToManyField(null=True, to='products.sizevarient'),
        ),
    ]
