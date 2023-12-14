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

urlpatterns = [
    path('', views.index, name='index'),
    path('enroll/', views.enroll_student, name='enroll_student'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('mark_attendance/<str:method>/', views.mark_attendance, name='mark_attendance'),
    path('attendance_history/', views.attendance_history, name='attendance_history'),
    path('enroll_rfid/', views.enroll_rfid, name='enroll_rfid'),
    path('validate_rfid/', views.validate_rfid, name='validate_rfid'),
    path('set/rfid/<int:access_code>/<str:tag_id>', views.set_rfid, name='set_rfid'),
    path('lecturer/login/', views.lecturer_login, name='lecturer_login'),
    # path('login/', views.login, name='login'),

]
