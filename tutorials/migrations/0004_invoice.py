# Generated by Django 5.1.2 on 2024-11-25 22:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0003_alter_lesson_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('orderNo', models.AutoField(primary_key=True, serialize=False)),
                ('topic', models.CharField(max_length=100)),
                ('no_of_classes', models.IntegerField()),
                ('price_per_class', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sum', models.DecimalField(decimal_places=2, max_digits=10)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorials.student')),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorials.tutor')),
            ],
        ),
    ]
