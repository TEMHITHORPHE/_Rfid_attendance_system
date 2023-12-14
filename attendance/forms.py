# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm


from .models import Student, Lecturer

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'student_id', 'fingerprint_id', 'rfid_id']



class LecturerLoginForm(AuthenticationForm):
    lecturer_id = forms.CharField(max_length=20)  # Add lecturer_id field

    class Meta:
        model = Lecturer
        fields = ('lecturer_id', 'password')