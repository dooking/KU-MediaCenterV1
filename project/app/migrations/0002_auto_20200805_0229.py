# Generated by Django 3.0.9 on 2020-08-04 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmentborrow',
            name='fromDateTime',
            field=models.IntegerField(max_length=50),
        ),
        migrations.AlterField(
            model_name='equipmentborrow',
            name='realDateTime',
            field=models.IntegerField(default=0, max_length=50),
        ),
        migrations.AlterField(
            model_name='equipmentborrow',
            name='toDateTime',
            field=models.IntegerField(max_length=50),
        ),
    ]
