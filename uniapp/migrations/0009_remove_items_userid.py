# Generated by Django 4.2.3 on 2023-10-12 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uniapp', '0008_items_userid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='items',
            name='userid',
        ),
    ]
