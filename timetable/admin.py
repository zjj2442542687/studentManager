from django.contrib import admin

# Register your models here.
from timetable.models import Timetable

admin.sites.reverse(Timetable)
