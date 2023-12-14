from django.contrib.auth.backends import ModelBackend
from .models import Lecturer

class LecturerIDBackend(ModelBackend):
    def authenticate(self, request, lecturer_id=None, password=None, **kwargs):
        try:
            lecturer = Lecturer.objects.get(lecturer_id=lecturer_id)
            if lecturer.check_password(password):
                return lecturer
        except Lecturer.DoesNotExist:
            return None
