# Generated by Django 3.0.9 on 2020-08-24 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20200824_1551'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipment',
            name='Borrow',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='Borrowed',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='willBorrow',
        ),
        migrations.RemoveField(
            model_name='equipmentborrow',
            name='Borrow',
        ),
        migrations.RemoveField(
            model_name='equipmentborrow',
            name='Borrowed',
        ),
        migrations.RemoveField(
            model_name='equipmentborrow',
            name='willBorrow',
        ),
        migrations.AddField(
            model_name='equipment',
            name='borrowState',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='equipmentborrow',
            name='borrowState',
            field=models.IntegerField(default=0),
        ),
    ]
