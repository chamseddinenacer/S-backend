# Generated by Django 3.2 on 2023-07-14 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appk', '0002_leaverequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaverequest',
            name='nbjour',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
