from django.urls import path
from .views import *
urlpatterns = [
    path("getMonthlySchedule/<slug:user_id>/",get_meeting_head_and_subhead),
    path("addDayEntries/",create_multiple_user_entries),
    path("getUserEntries/",get_entries),
    path("changeStatus/<int:user_entry_id>/",change_status),
    path("addMeetingHeadSubhead/",add_meeting_head_subhead),
]
