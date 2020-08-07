# Generated by Django 3.0.9 on 2020-08-06 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200805_0229'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equipmentborrow',
            old_name='division',
            new_name='auth',
        ),
        migrations.RenameField(
            model_name='equipmentborrow',
            old_name='goal',
            new_name='group',
        ),
        migrations.RemoveField(
            model_name='equipmentborrow',
            name='isCard',
        ),
        migrations.AddField(
            model_name='equipmentborrow',
            name='purpose',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='equipmentborrow',
            name='remark',
            field=models.CharField(default='', max_length=50),
        ),
    ]