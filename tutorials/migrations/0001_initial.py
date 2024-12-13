# Generated by Django 5.1.2 on 2024-12-13 14:23

import django.contrib.auth.models
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(message='Username must consist of @ followed by at least three alphanumericals', regex='^@\\w{3,}$')])),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('date_of_birth', models.DateField(default='2000-01-01')),
                ('type_of_user', models.CharField(choices=[('admin', 'Admin'), ('tutor', 'Tutor'), ('student', 'Student')], default='student', max_length=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('tutorials.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone', models.CharField(default='07777777777', max_length=12)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('tutorials.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('bio', models.CharField(blank=True, max_length=520, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('tutorials.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=100, unique=True)),
                ('timings', models.CharField(blank=True, max_length=255)),
                ('bio', models.CharField(blank=True, max_length=520, null=True)),
                ('tutor_list', models.JSONField(default=list)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('resolved', 'Resolved')], default='pending', max_length=20)),
                ('admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tutorials.admin')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='tutorials.student')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('orderNo', models.AutoField(primary_key=True, serialize=False)),
                ('topic', models.CharField(max_length=100)),
                ('no_of_classes', models.IntegerField()),
                ('price_per_class', models.DecimalField(decimal_places=2, default=20, max_digits=10)),
                ('total_sum', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorials.student')),
            ],
        ),
        migrations.CreateModel(
            name='TutorAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('all', 'All'), ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday'), ('sunday', 'Sunday')], max_length=10)),
                ('starttime', models.TimeField()),
                ('endtime', models.TimeField()),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorials.tutor')),
            ],
        ),
        migrations.AddField(
            model_name='tutor',
            name='subjects',
            field=models.ManyToManyField(related_name='tutors', to='tutorials.subjects'),
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('lesson_id', models.AutoField(primary_key=True, serialize=False)),
                ('day_of_week', models.CharField(choices=[('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday'), ('sunday', 'Sunday')], max_length=10)),
                ('start_time', models.TimeField()),
                ('duration', models.IntegerField(choices=[(60, '1 hour'), (120, '2 hours')], default=60)),
                ('frequency', models.CharField(choices=[('weekly', 'Weekly'), ('fortnightly', 'Fortnightly')], max_length=20)),
                ('term', models.CharField(choices=[('September-Christmas', 'September-Christmas'), ('January-Easter term', 'January-Easter'), ('May-July', 'May-July')], max_length=50)),
                ('subject', models.CharField(choices=[('ruby_on_rails', 'Ruby on Rails'), ('python', 'Python'), ('javascript', 'Javascript'), ('c_plus_plus', 'C++'), ('c_sharp', 'C#'), ('react', 'React'), ('angular', 'Angular'), ('vue_js', 'Vue.js'), ('node_js', 'Node.js'), ('express_js', 'Express.js'), ('django', 'Django'), ('flask', 'Flask'), ('spring', 'Spring'), ('hibernate', 'Hibernate'), ('jpa', 'JPA'), ('sql', 'SQL'), ('mongodb', 'MongoDB'), ('postgresql', 'PostgreSQL'), ('mysql', 'MySQL'), ('git', 'Git')], max_length=100)),
                ('status', models.CharField(choices=[('Rejected', 'Rejected'), ('pending', 'Pending'), ('confirmed', 'Confirmed'), ('late', 'Late')], default='Pending', max_length=20)),
                ('payment_status', models.CharField(choices=[('Unpaid', 'Unpaid'), ('Paid', 'Paid')], default='Unpaid', max_length=10)),
                ('invoice_no', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tutorials.invoice')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='tutorials.student')),
                ('tutor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lessons', to='tutorials.tutor')),
            ],
        ),
        migrations.AddField(
            model_name='invoice',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorials.tutor'),
        ),
    ]
