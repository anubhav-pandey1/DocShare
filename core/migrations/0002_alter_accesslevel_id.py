# Generated by Django 4.0.4 on 2022-05-20 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesslevel',
            name='id',
            field=models.IntegerField(choices=[(1, 'Unauthorized'), (10, 'Viewer'), (50, 'Editor'), (100, 'Owner')], primary_key=True, serialize=False, unique=True),
        ),
    ]
