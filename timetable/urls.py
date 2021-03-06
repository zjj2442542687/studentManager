from django.urls import path
from timetable.views.timetable_insert import TimetableInsertView, TimetableInsertFileView
from timetable.views.timetable_select import TimetableSelectView

urlpatterns = [
    # 导入课表
    path("insert", TimetableInsertView.as_view({'post': 'create'})),
    path("addCourse", TimetableInsertView.as_view({'post': 'add_course'})),
    path("insertFile", TimetableInsertFileView.as_view({'post': 'batch_import'})),
    path("selectClass", TimetableSelectView.as_view({'post': 'select_class'})),
    path("selectStudentTimetableByToken", TimetableSelectView.as_view({'post': 'select_student_timetable_by_token'})),
]
