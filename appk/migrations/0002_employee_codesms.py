# Generated by Django 3.2.20 on 2023-09-15 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='codesms',
            field=models.CharField(default='', max_length=10),
        ),
    ]