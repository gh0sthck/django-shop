# Generated by Django 5.0.1 on 2024-01-28 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0003_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/'),
        ),
    ]
