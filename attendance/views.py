# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Student, Attendance
from .forms import StudentForm
from django.views.decorators.csrf import csrf_exempt



RFID_TAG_ID = -1;

@csrf_exempt
def index(request):
    return render(request, 'index.html')

@csrf_exempt



def attendance_history(request):
    # TODO: Implement logic to retrieve and display attendance history
    return render(request, 'attendance_history.html', {'attendance_history': []})


@csrf_exempt
def enroll_rfid(request):
    if (request.method == 'POST'):
        return JsonResponse({
            'status': 'true' if RFID_TAG_ID != -1 else 'false' ,
            'tag_id': RFID_TAG_ID
            })


def validate_rfid(request):
    if request.method == 'POST':
        try:
            # Assuming the RFID UID is sent as 'uid' in the POST data
            rfid_uid = request.POST['uid']
            
            # TODO: Validate rfid_uid and perform necessary actions

            # For demonstration, let's just return a success response
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



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
        # TODO: Implement login/authentication logic
        return render(request, 'dashboard.html', {'attendance_records': []})
    return render(request, 'login.html')



def dashboard(request):
    # TODO: Retrieve attendance records for the logged-in student
    # ...
    return render(request, 'dashboard.html', {'attendance_records': []})



def mark_attendance(request, method):
    if method == 'fingerprint':
        # TODO: Implement fingerprint verification logic
        # ...
        pass
    elif method == 'rfid':
        # TODO: Implement RFID verification logic
        # ...
        pass
    return render(request, 'mark_attendance.html')
