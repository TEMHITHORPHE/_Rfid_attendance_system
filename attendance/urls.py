""" from django.urls import path
from . import views

urlpatterns = [
    path('student_list/', views.student_list, name='student_list'),
    path('add_student/', views.add_student, name='add_student'),
]
 """
 
 
from django.urls import path
from . import views
# from .views import validate_rfid, enroll_rfid, set_rfid, 

app_name = 'attendance'


urlpatterns = [
    path('', views.index, name='index'),
    path('enroll/', views.enroll_student, name='enroll_student'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('mark_attendance/rfid/<int:access_code>/<str:tag_id>', views.mark_attendance, name='mark_attendance'),    # Used By Arduino
    path('set/rfid/<int:access_code>/<str:tag_id>', views.set_rfid, name='set_rfid'),   # Used by Arduino.
    path('retrieve/rfid/', views.retrieve_rfid, name='retrieve_rfid'),  # Used during student enrolling (Ajax Calls)
    path('retrieve/live/attendance/', views.retrieve_live_attendance, name='retrieve_live_attendance'), # (Ajax Calls)
    path('lecturer/login/', views.lecturer_login, name='lecturer_login'),
    path('lecturer/attendance/live/', views.live_attendance, name='live_attendance')
]