# Generated by Django 4.1.2 on 2022-10-09 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_alter_product_details_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_details',
            name='product_title',
            field=models.CharField(max_length=300),
        ),
    ]
