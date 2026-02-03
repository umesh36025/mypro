from rest_framework.viewsets import ModelViewSet
import requests
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Holiday, BookSlot, Tour, Event, Room, BookingStatus
from .serializers import (
    HolidaySerializer,
    BookSlotSerializer,
    TourSerializer,
    EventSerializer,
    RoomSerializer,
    BookingStatusSerializer
)

class BookSlotViewSet(ModelViewSet):
    queryset = BookSlot.objects.all()
    serializer_class = BookSlotSerializer

@api_view(["GET"])
def rooms_dropdown(request):
    rooms = Room.objects.filter(is_active=True)
    serializer = RoomSerializer(rooms, many=True)
    return Response({
        "status": "success",
        "data": serializer.data
    })

class TourViewSet(ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

class HolidayViewSet(ModelViewSet):
    queryset = Holiday.objects.all().order_by("date")
    serializer_class = HolidaySerializer

    # ✅ /api/holidays/fixed/
    @action(detail=False, methods=["get"], url_path="fixed")
    def fixed_holidays(self, request):
        qs = self.queryset.filter(holiday_type="fixed")
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    # ✅ /api/holidays/unfixed/
    @action(detail=False, methods=["get"], url_path="unfixed")
    def unfixed_holidays(self, request):
        qs = self.queryset.filter(holiday_type="unfixed")
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

@api_view(["GET"])
def status_dropdown(request):
    status = BookingStatus.objects.filter(is_active=True)
    serializer = BookingStatusSerializer(status, many=True)
    return Response({
        "status": "success",
        "data": serializer.data
    })

@api_view(["GET"])
def location_dropdown(request):
    query = request.GET.get("q")
    if not query:
        return Response({"status": "success", "data": []})

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "limit": 8
    }

    headers = {
        "User-Agent": "calendar-backend"
    }

    res = requests.get(url, params=params, headers=headers, timeout=5)
    data = res.json()

    results = [
        {
            "label": place["display_name"],
            "value": place["display_name"]
        }
        for place in data
    ]

    return Response({
        "status": "success",
        "data": results
    })