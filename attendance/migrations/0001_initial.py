# Generated by Django 5.0 on 2023-12-14 19:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('staff_id', models.CharField(max_length=12, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('student_id', models.CharField(max_length=10, unique=True)),
                ('fingerprint_id', models.CharField(default=None, max_length=10, unique=True)),
                ('rfid_id', models.CharField(max_length=12, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_title', models.CharField(max_length=50)),
                ('course_code', models.PositiveSmallIntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('lecture', 'Lecture'), ('exam', 'Exam'), ('test', 'Test')], max_length=10)),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='attendance.lecturer')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='attendance.student')),
            ],
        ),
    ]
