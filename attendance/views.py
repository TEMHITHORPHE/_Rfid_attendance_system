# views.py
from django.db import transaction
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import StudentForm
from .models import Student, Attendance, AttendanceConfig



ACCESS_CODE = 1234
ENROLLMENT_RFID_TAG_ID = -1;

# E -> Enrollment Mode,    A -> Attendance Mode
RFID_TAG_SUBMISSION_MODE = 'E'

# A hack to get around arduino not knowing anything about the logged in lecturer.
LIVE_ATTENDANCE_ID = None


@csrf_exempt
def index(request):
    return render(request, 'index.html')



# Called By Arduino
def rfid_submission_mode(request, access_code):
    print("[[[[[[[ CONFIG MODE REQUEST ]]]]]]]]]")
    if (request.method == 'GET' and access_code == ACCESS_CODE ):
        return HttpResponse(content=RFID_TAG_SUBMISSION_MODE);
    return HttpResponseNotAllowed(['GET'])



# Called By Arduino
def set_rfid(request, access_code, tag_id):
    global ENROLLMENT_RFID_TAG_ID
    print("[RFID ENROLL]: ", access_code, tag_id);

    if (request.method == 'GET' and access_code == ACCESS_CODE ):
        ENROLLMENT_RFID_TAG_ID = tag_id
        print("[RFID TAG ID - SUCCESS]::: ", tag_id)
        return JsonResponse({
            'status': 'success',
        })
    return HttpResponseNotAllowed(['GET'])



# Ajax Calls Only
@csrf_exempt
def retrieve_rfid(request):
    if (request.method == 'POST'):
        print(request)
        return JsonResponse({
            'status': 'true' if ENROLLMENT_RFID_TAG_ID != -1 else 'false' ,
            'tag_id': ENROLLMENT_RFID_TAG_ID
            })



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
    if (request.method == 'POST'):
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # Redirect to dashboard after login
                return redirect('/dashboard')
            else:
                return render(request, 'lecturer_login.html', {'login_error': True})
    else:
        form = AuthenticationForm()
    return render(request, 'lecturer_login.html', {'form': form})


@login_required(login_url=('/lecturer/login/'))
@transaction.atomic
@csrf_exempt
def dashboard(request):
    if (request.method == 'GET'):
        if (not request.user.is_authenticated):
            # return redirect('/lecturer/login/')
            return redirect(reverse('lecturer_login'))

        user = request.user  # This will return current authenticated user
        lecturer = User.objects.get(id=user.id)

        # Retrieve AttendanceConfig for the lecturer
        attendance_config, created = AttendanceConfig.objects.get_or_create(lecturer=lecturer,  defaults={ 'config': {'live_attendance': False } } )

        if (not created): LIVE_ATTENDANCE_ID = attendance_config.config['attendance_id']

        # Query all attendances related to the specified lecturer (descending order, oldest attendance first).
        attendances = Attendance.objects.filter(lecturer=lecturer).order_by('-date').prefetch_related('student').all()
        print("[Student Attendances]: ", attendances )

        return render(request, 'dashboard.html', {'config': attendance_config.config, 'attendances': attendances})
    
    elif (request.method == 'POST'):
        
        # Get "Attendance" entries with an empty 'student' field and delete them
        Attendance.objects.filter(student__isnull=True).delete();   # (Ideally, should be a non regular cron job).

        # Extract data from the form
        course_title = request.POST.get('course_title')
        course_code = request.POST.get('course_code')
        status = request.POST.get('status')

        user = request.user
        lecturer = User.objects.get(id=user.id)

        # Create a New Attendance Entry
        attendance = Attendance.objects.create(course_title=course_title, course_code=course_code, status=status, lecturer=lecturer)
        # {'live_attendance': True, 'attendance_id': 33, 'status': 'lecture', 'course_title': Information Systems, 'course_code': CIT513}


        config_data = {
            'live_attendance': True,  'attendance_id': attendance.id, 'status': status,
            'course_title': course_title, 'course_code': course_code
        }

        # Update Attendance Configurations with New Entry
        attendance_config, _ = AttendanceConfig.objects.get_or_create(lecturer=lecturer,  defaults={ 'config': {'live_attendance': False } } )
        attendance_config.config = config_data;
        attendance_config.save(force_update=True)
    
        redirect(reverse('attendance:live_attendance'))
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])



@login_required(login_url='lecturer_login')
def live_attendance(request):
    global LIVE_ATTENDANCE_ID

    if (request.method == 'GET'):
        user = request.user
        lecturer = User.objects.get(id=user.id)

        # Retrieve AttendanceConfig for the lecturer
        attendance_config, created = AttendanceConfig.objects.get_or_create(lecturer=lecturer,  defaults={ 'config': {'live_attendance': False } } )
        # {'live_attendance': True, 'attendance_id': 33, 'status': 'lecture', 'course_title': Information Systems, 'course_code': CIT513}

        if (not created): LIVE_ATTENDANCE_ID = attendance_config.config['attendance_id']

        # Retrieve current Attendance based on the live attendance id gotten from AttendanceConfig.
        ongoing_attendance = Attendance.objects.get(lecturer=lecturer, id=attendance_config.config['attendance_id']).student.all()
        print("[Live Attendance]: ", ongoing_attendance )

        return render(request, 'live_attendance.html', {'config': attendance_config.config, 'attendance': ongoing_attendance})
    
    elif (request.method == 'POST'):    # Only called to end live/Ongoing attendance.
        user = request.user
        lecturer = User.objects.get(id=user.id)

        # Retrieve AttendanceConfig for the lecturer
        attendance_config, created = AttendanceConfig.objects.get_or_create(lecturer=lecturer,  defaults={ 'config': {'live_attendance': False } } )
        # {'live_attendance': True, 'attendance_id': 33, 'status': 'lecture', 'course_title': Information Systems, 'course_code': CIT513}

        if (not created):
            attendance_config.config = {
                **attendance_config.config,
                'live_attendance': False,
                'attendance_id': None
            }
        
        LIVE_ATTENDANCE_ID = None
        
        attendance_config.save();
        redirect(reverse('attendance:dashboard'))
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])



# Called By Arduino
def mark_attendance(request, access_code, tag_id):

    if (request.method == 'GET'):
        print("[Marking Attendance]: ", tag_id)
        if (access_code != ACCESS_CODE): return JsonResponse({'status': 'error', 'msg': 'Invalid Acess Code!'})
        if (LIVE_ATTENDANCE_ID == None): return JsonResponse({'status': 'error', 'msg': 'No Live Attendance In Session!!!!'})

        try:
            # lecturer = User.objects.get(id=LIVE_ATTENDANCE_ID)
            # attendance_config = AttendanceConfig.objects.get(lecturer=lecturer)

            student = Student.objects.get(rfid_id=tag_id)   # Retrieve Student based on tag ID.
            attendance = Attendance.objects.get(id=LIVE_ATTENDANCE_ID)    # Get curent/live attendance
            attendance.student.add(student) # Add student to attendance list.
            attendance.save();

            return JsonResponse({
                'status': 'success',
                'msg': 'Attendance Recorded!'
            })
        
        except Student.DoesNotExist:
            return JsonResponse({'status': 'error', 'msg': 'Unrecognized Student RFID TAG!'})
        except AttendanceConfig.DoesNotExist or Attendance.DoesNotExist:
            return JsonResponse({'status': 'error', 'msg': 'No Live Attendance In Session!'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'msg': 'Strange ... Unknown Lecturer ID!'})
        except Exception as error:
            print("[Error Marking Attendance]: ", error)
            return JsonResponse({'status': 'error', 'msg': 'Unexpected! Error! occured!'})
    
    return HttpResponseNotAllowed(['GET'])



# Ajax Calls Only
@login_required(login_url='lecturer_login')
@csrf_exempt
def retrieve_live_attendance(request, skip_count):
    print(LIVE_ATTENDANCE_ID, skip_count)
    try:
        if (request.method == 'POST'):
            attendance = Attendance.objects.get(id=LIVE_ATTENDANCE_ID)
            students = list(attendance.student.all().values())[skip_count:]
            print("[Attendance-Ajax]:", students)
            return JsonResponse({
                'status': 'success',
                'attendance': students
            })
    except Exception as error:
        print(error)
        return JsonResponse({
                'status': 'error',
                'attendance': None
        })
