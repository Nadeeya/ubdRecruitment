from django.contrib import admin
from .models import Recruiter , Job , Application , UserFile

# Register your models here.
admin.site.register(Recruiter)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(UserFile)
