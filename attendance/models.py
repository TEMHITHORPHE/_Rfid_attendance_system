# models.py
from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    student_id = models.CharField(primary_key=True, max_length=10, unique=True) # Primary Key
    fingerprint_id = models.CharField(max_length=10, unique=True, default=None)
    rfid_id = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class AttendanceConfig(models.Model):
    lecturer = models.OneToOneField(User, on_delete=models.PROTECT, unique=True)
    config = models.JSONField();
    # {'live_attendance': True, 'attendance_id': 33, 'status': 'lecture', 'course_title': Information Systems, 'course_code': CIT513}   


class Attendance(models.Model):
    course_title = models.CharField(max_length=50, blank=False)
    course_code = models.CharField(max_length=7, blank=False)
    student = models.ManyToManyField(Student, blank=True)
    lecturer = models.ForeignKey(User, on_delete=models.PROTECT, blank=False)
    date = models.DateTimeField(auto_now_add=True, blank=False)
    status = models.CharField(choices=[('lecture', 'Lecture'), ('exam', 'Exam'), ('test', 'Test')], max_length=10, blank=False)



    def __str__(self):
        student = self.student.all()
        return f'{student}'
