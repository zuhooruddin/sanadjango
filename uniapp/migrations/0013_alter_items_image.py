# Generated by Django 4.2.3 on 2023-10-12 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uniapp', '0012_items_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='image',
            field=models.ImageField(upload_to='media/image/'),
        ),
    ]
