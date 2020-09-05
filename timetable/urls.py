from django.urls import path
from timetable.views.timetable_insert import TimetableInsertView
from timetable.views.timetable_select import TimetableSelectView

urlpatterns = [
    path("insert", TimetableInsertView.as_view({'post': 'create'})),
    path("addCourse", TimetableInsertView.as_view({'post': 'add_course'})),
    path("selectClass", TimetableSelectView.as_view({'post': 'select_class'})),
    path("selectStudentTimetableByToken", TimetableSelectView.as_view({'post': 'select_student_timetable_by_token'})),
]
