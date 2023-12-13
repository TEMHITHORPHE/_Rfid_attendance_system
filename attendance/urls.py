""" from django.urls import path
from . import views

urlpatterns = [
    path('student_list/', views.student_list, name='student_list'),
    path('add_student/', views.add_student, name='add_student'),
]
 """
 
 
from django.urls import path
from . import views
from .views import validate_rfid

urlpatterns = [
    path('', views.index, name='index'),
    path('enroll/', views.enroll_student, name='enroll_student'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('mark_attendance/<str:method>/', views.mark_attendance, name='mark_attendance'),
    path('attendance_history/', views.attendance_history, name='attendance_history'),
    path('validate_rfid/', validate_rfid, name='validate_rfid'),
]
