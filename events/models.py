from django.db import models
import datetime
from accounts.models import User

# ========================
# MASTER TABLES
# ========================

class Room(models.Model):
    name= models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table='events"."Rooms'
        verbose_name="Room"
        verbose_name_plural = "rooms"

    def __str__(self):
        return self.name


class BookingStatus(models.Model):
    status_name = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table='events"."BookingStatus'
        verbose_name="bookingstatus"

    def __str__(self):
        return self.status_name

# ========================
# 1. BOOK SLOT
# ========================

class BookSlot(models.Model):

    meeting_title = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    description = models.TextField(blank=True, null=True)
    MEETING_TYPE_CHOICES = [
        ("individual", "Individual"),
        ("group", "Group Meeting"),
    ]
    meeting_type = models.CharField(
        max_length=20,
        choices=MEETING_TYPE_CHOICES
    )
    status = models.ForeignKey(
        BookingStatus,
        on_delete=models.CASCADE,
        related_name="bookings",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table='events"."Slots'
        verbose_name="Slot"

    def __str__(self):
        return self.meeting_title

# ========================
# 2. TOUR
# ========================

class Tour(models.Model):
    tour_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    duration_days = models.PositiveIntegerField()
    starting_date = models.DateField(blank=True, null=True)
    member=models.ManyToManyField(User,through="tourMembers",related_name="members")
    # checkbox list (empty allowed)
    total_members=models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='events"."Tour'
        verbose_name="tour"
        ordering=["-starting_date"]
    def __str__(self):
        return self.tour_name

class tourmembers(models.Model):
    tour=models.ForeignKey(Tour,on_delete=models.CASCADE)
    member=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    
    class Meta:
        db_table='events"."tourmembers'
        verbose_name="tourmember"
        unique_together = ("tour", "member")
        ordering=["tour"]
# ========================
# 3. HOLIDAY
# ========================

class Holiday(models.Model):
    FIXED = "fixed"
    UNFIXED = "unfixed"

    HOLIDAY_TYPE_CHOICES = [
        (FIXED, "Fixed"),
        (UNFIXED, "Unfixed"),
    ]

    date = models.DateField()
    name = models.CharField(max_length=255)
    holiday_type = models.CharField(
        max_length=10,
        choices=HOLIDAY_TYPE_CHOICES,
        default=UNFIXED
    )
    
    class Meta:
        db_table='task_management"."Holiday'
        verbose_name="Holiday"
        verbose_name_plural = "Holiday"
        ordering=["date"]

    def __str__(self):
        return f"{self.name}-{self.date}"

# ========================
# 4. EVENTS
# ========================

class Event(models.Model):              
    title = models.CharField(max_length=255, default="Untitled Event")
    motive = models.TextField(null=True)
    date = models.DateField()
    time = models.TimeField()  
    
    class Meta:
        db_table='task_management"."Event'
        verbose_name="Event"
        ordering=["date"]               

    def __str__(self):
        return self.title