# models.py
from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    student_id = models.CharField(max_length=10, unique=True)
    fingerprint_id = models.CharField(max_length=10, unique=True, default=None)
    rfid_id = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



# class Lecturer(models.Model):
#     id = models.AutoField(primary_key=True)
#     staff_id = models.CharField(max_length=12, unique=True)


class Attendance(models.Model):
    course_title = models.CharField(max_length=50, blank=False)
    course_code = models.CharField(max_length=7, blank=False)
    student = models.ForeignKey(Student, on_delete=models.PROTECT, blank=False)
    lecturer = models.ForeignKey(User, on_delete=models.PROTECT, blank=False)
    date = models.DateTimeField(auto_now_add=True, blank=False)
    status = models.CharField(choices=[('lecture', 'Lecture'), ('exam', 'Exam'), ('test', 'Test')], max_length=10, blank=False)



    def __str__(self):
        return f'{self.course_code}_{self.student.first_name}_{self.student.last_name}_{self.date}'

