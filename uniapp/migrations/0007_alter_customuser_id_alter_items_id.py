# Generated by Django 4.2.3 on 2023-10-09 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uniapp', '0006_remove_items_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='items',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
