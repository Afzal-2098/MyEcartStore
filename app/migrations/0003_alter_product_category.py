# Generated by Django 4.0.4 on 2022-09-11 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_placedorder_status_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('mobile', 'Mobile'), ('laptop', 'Laptop'), ('top Wear', 'Top Wear'), ('bottom Wear', 'Bottom Wear'), ('mens wear', 'Mens Wear'), ('womens wear', 'Womens Wear'), ('kids wear', 'Kids Wear'), ('footwear', 'Footwear'), ('furniture', 'Furniture'), ('grocery', 'Grocery'), ('electronics', 'Electronics'), ('grooming', 'Grooming'), ('toy', 'Toy'), ('fashion', 'Fashion')], max_length=50),
        ),
    ]
