# Generated by Django 5.1.2 on 2024-11-25 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
