# Generated by Django 3.2.16 on 2022-10-17 05:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_addtocart_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(blank=True, max_length=150, null=True)),
                ('city', models.CharField(blank=True, max_length=150, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('zip', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('payment_method', models.CharField(choices=[('cod', 'cod'), ('upi', 'upi')], max_length=100)),
                ('delivery_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.address')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.product_details')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='myuser',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='App.address'),
        ),
    ]