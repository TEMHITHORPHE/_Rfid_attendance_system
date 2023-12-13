# models.py
from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    student_id = models.CharField(max_length=10, unique=True)
    fingerprint_id = models.CharField(max_length=10, unique=True, default=None)
    rfid_id = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.student.first_name} {self.student.last_name} - {self.date}'
