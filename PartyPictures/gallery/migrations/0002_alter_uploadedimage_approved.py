# Generated by Django 5.2 on 2025-04-21 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedimage',
            name='approved',
            field=models.BooleanField(default=True),
        ),
    ]
