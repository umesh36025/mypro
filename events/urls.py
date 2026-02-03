from rest_framework.routers import DefaultRouter
from django.urls import path, include


from .views import (
    rooms_dropdown,
    status_dropdown,
    location_dropdown,
    BookSlotViewSet,
    TourViewSet,
    HolidayViewSet,
    EventViewSet,
    RoomViewSet,
    BookingStatusViewset
    

)

router = DefaultRouter()
router.register("bookslots", BookSlotViewSet, basename="bookslots")
router.register("tours", TourViewSet, basename="tours")
router.register("holidays", HolidayViewSet, basename="holidays")
router.register("events", EventViewSet, basename="events")
router.register("rooms", RoomViewSet, basename="rooms")
router.register("status", BookingStatusViewset, basename="status")

urlpatterns = [
    path("", include(router.urls)),
]