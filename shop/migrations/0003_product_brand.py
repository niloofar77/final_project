# Generated by Django 2.2.13 on 2021-01-04 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20200324_0719'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]