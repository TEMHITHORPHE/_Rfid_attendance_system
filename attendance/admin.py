from django.contrib import admin

from .models import Student, Attendance, Lecturer

# Register your models here.
admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(Lecturer)


# Register other models as needed
