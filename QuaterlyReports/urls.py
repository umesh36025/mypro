from django.urls import path
from .views import *
urlpatterns = [
    path("getMonthlySchedule/<slug:user_id>/",get_meeting_head_and_subhead),
    path("addDayEntries/",create_multiple_user_entries),
    path("getUserEntries/",get_entries),
]
