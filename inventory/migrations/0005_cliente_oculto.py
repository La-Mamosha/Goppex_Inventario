# Generated by Django 5.1 on 2024-10-01 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_producto_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='oculto',
            field=models.BooleanField(default=False),
        ),
    ]
