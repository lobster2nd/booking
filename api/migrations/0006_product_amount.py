# Generated by Django 4.2.2 on 2023-08-29 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_product_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='amount',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
