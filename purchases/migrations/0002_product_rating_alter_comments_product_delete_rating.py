# Generated by Django 5.0.2 on 2024-05-08 10:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='comments',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', related_query_name='comment', to='purchases.product', verbose_name='Товар'),
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]