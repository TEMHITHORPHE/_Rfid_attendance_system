# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


from .forms import StudentForm, LecturerLoginForm
from .models import Student, Attendance, Lecturer



RFID_TAG_ID = -1;
ACCESS_CODE = 123456789097654321

@csrf_exempt
def index(request):
    return render(request, 'index.html')

@csrf_exempt



def attendance_history(request):
    # TODO: Implement logic to retrieve and display attendance history
    return render(request, 'attendance_history.html', {'attendance_history': []})


def set_rfid(request, access_code, tag_id):
    global RFID_TAG_ID
    print(request, access_code, tag_id, type(tag_id));
    if (request.method == 'GET' and access_code == ACCESS_CODE ):
        RFID_TAG_ID = tag_id
        print("[RFID TAG ID - UPDATE]::: ", RFID_TAG_ID)
        return JsonResponse({
            'status': 'success',
        })


@csrf_exempt
def enroll_rfid(request):
    if (request.method == 'POST'):
        print(request)
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




def lecturer_login(request):
    if request.method == 'POST':
        form = LecturerLoginForm(request, data=request.POST)
        if form.is_valid():
            lecturer_id = form.cleaned_data['lecturer_id']
            password = form.cleaned_data['password']
            user = authenticate(request, lecturer_id=lecturer_id, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to lecturer's dashboard or any desired page
    else:
        form = LecturerLoginForm()
    return render(request, 'lecturer_login.html', {'form': form})



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
