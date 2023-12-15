# views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import StudentForm
from .models import Student, Attendance



RFID_TAG_ID = -1;
ACCESS_CODE = 1234

@csrf_exempt
def index(request):
    return render(request, 'index.html')



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
            return render(request, 'enroll.html', {'student': { 'enrolled': True, 'name': request.POST['first_name'] } })
        return render(request, 'enroll.html', {'student': { 'enrolled': False } })
    else:
        form = StudentForm()
    return render(request, 'enroll.html', {'form': form})




def lecturer_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # Redirect to a success page or homepage after login
                return redirect('/dashboard')
            else:
                return render(request, 'lecturer_login.html', {'login_error': True})
    else:
        form = AuthenticationForm()
    return render(request, 'lecturer_login.html', {'form': form})



@login_required(login_url='lecturer_login')
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
