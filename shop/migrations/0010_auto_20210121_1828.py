# Generated by Django 2.2.13 on 2021-01-21 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_product_deleted'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookmark',
            options={},
        ),
        migrations.AddField(
            model_name='bookmark',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
