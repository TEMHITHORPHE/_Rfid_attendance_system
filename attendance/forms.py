# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login


from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'student_id', 'fingerprint_id', 'rfid_id']



# class LecturerForm(forms.ModelForm):
#     class Meta:
#         model = Lecturer
#         fields = ['staff_id']
