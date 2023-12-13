""" from django.shortcuts import render, redirect
from .models import Student
from .forms import StudentForm

def student_list(request):
    students = Student.objects.all()
    return render(request, 'attendance/student_list.html', {'students': students})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'attendance/add_student.html', {'form': form})
 """

""" 
from django.shortcuts import render, redirect
from .models import Student, Attendance
from .forms import StudentForm
from django.contrib.auth import authenticate, login


def index(request):
    return render(request, 'index.html')

def enroll_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'dashboard.html', {'attendance_records': []})
    else:
        form = StudentForm()
    return render(request, 'enroll.html', {'form': form})

def login(request):
    if request.method == 'POST':
        # Implement login logic here
        # ...
        return render(request, 'dashboard.html', {'attendance_records': []})
    return render(request, 'login.html')

def dashboard(request):
    # Retrieve attendance records for the logged-in student
    # ...
    return render(request, 'dashboard.html', {'attendance_records': []})

def mark_attendance(request, method):
    if method == 'fingerprint':
        # Implement fingerprint verification logic
        # ...
        pass
    elif method == 'rfid':
        # Implement RFID verification logic
        # ...
        pass
    return render(request, 'mark_attendance.html')
    

def attendance_history(request):
    # Retrieve attendance history for the logged-in student
    # ...
    return render(request, 'attendance_history.html', {'attendance_history': []})

def student_list(request):
    students = Student.objects.all()
    return render(request, 'attendance/student_list.html', {'students': students})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'attendance/add_student.html', {'form': form})
 """
 
 
 
 
from django.shortcuts import render
from .models import Student, Attendance
from .forms import StudentForm


def index(request):
    return render(request, 'index.html')

""" def enroll_student(request):
    if request.method == 'POST':
        # Process form submission and create a new student
        # ...
        return render(request, 'dashboard.html', {'attendance_records': []})
    return render(request, 'enroll.html') """
    
    
def enroll_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            # Step 1: Extract Form Data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            date_of_birth = form.cleaned_data['date_of_birth']
            student_id = form.cleaned_data['student_id']
            fingerprint_id = form.cleaned_data['fingerprint_id']
            rfid_id = form.cleaned_data['rfid_id']
            
            # Step 3: Create a New Student
            student = Student(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                student_id=student_id,
                fingerprint_id=fingerprint_id,
                rfid_id=rfid_id
            )
            
            # Step 4: Save the Student Object
            student.save()
            
            # Step 5: Render Dashboard
            return render(request, 'dashboard.html', {'attendance_records': []})
    else:
        form = StudentForm()
    return render(request, 'enroll.html', {'form': form})


def login(request):
    if request.method == 'POST':
        # Process form submission and authenticate the student
        # ...
        return render(request, 'dashboard.html', {'attendance_records': []})
    return render(request, 'login.html')

def dashboard(request):
    # Retrieve attendance records for the logged-in student
    # ...
    return render(request, 'dashboard.html', {'attendance_records': []})

def mark_attendance(request, method):
    if method == 'fingerprint':
        # Implement fingerprint verification logic
        # ...
        pass
    elif method == 'rfid':
        # Implement RFID verification logic
        # ...
        pass
    return render(request, 'mark_attendance.html')

def attendance_history(request):
    # Retrieve attendance history for the logged-in student
    # ...
    return render(request, 'attendance_history.html', {'attendance_history': []})
