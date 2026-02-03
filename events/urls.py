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
)

router = DefaultRouter()
router.register("bookslots", BookSlotViewSet, basename="bookslots")
router.register("tours", TourViewSet, basename="tours")
router.register("holidays", HolidayViewSet, basename="holidays")
router.register("events", EventViewSet, basename="events")

urlpatterns = [
    path("rooms/", rooms_dropdown, name="rooms-dropdown"),
    path("status/", status_dropdown, name="status-dropdown"),
    path("locations/", location_dropdown, name="location-dropdown"),
    path("", include(router.urls)),
]