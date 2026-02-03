from rest_framework import serializers
from .models import *
from django.shortcuts import get_object_or_404
from django.http import Http404,JsonResponse,HttpRequest
from accounts.filters import get_users_Name
class SlotMemberSerializer(serializers.ModelSerializer):
    member=serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="username")
    class Meta:
        model = SlotMembers
        fields = ['member']
        
class BookSlotSerializer(serializers.ModelSerializer):
    status= serializers.SlugRelatedField(
        queryset=BookingStatus.objects.all(),
        slug_field="status_name"
    )
    room= serializers.SlugRelatedField(
        queryset=Room.objects.all(),
        slug_field="name")
    
    members = serializers.SlugRelatedField(
        many=True,
        slug_field='username',
        queryset=User.objects.all()
    )
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    creator_username = serializers.ReadOnlyField(source='created_by.username')
    member_details = serializers.SerializerMethodField()
    class Meta:
        model = BookSlot
        fields = [
            'id', 'meeting_title', 'date', 'start_time', 'end_time', 
            'room', 'description', 'meeting_type', 'status', 
            'created_at',"created_by","creator_username", 'member_details'
        ]
        
    def get_member_details(self, obj):
        # Accesses the ManyToMany relationship
        return [
            {
                "username": user.username,
                "full_name": get_users_Name(user) # fallback if name is empty
            } 
            for user in obj.members.all()]
        

    def create(self, validated_data):
        # Extract the list of user objects identified by username
        member_users = validated_data.pop('members', [])
        print(validated_data)
        # Create the BookSlot instance
        book_slot = BookSlot.objects.create(**validated_data)
        
        # Manually create entries in the through table
        for user in member_users:
            SlotMembers.objects.create(slot=book_slot, member=user)
            
        return book_slot

    def update(self, instance, validated_data):
        member_users = validated_data.pop('members', None)
        
        # Standard update for BookSlot fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # If members were provided in the request, replace the old ones
        if member_users is not None:
            instance.slotmembers_set.all().delete()
            for user in member_users:
                SlotMembers.objects.create(slot=instance, member=user)
        
        return instance
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "name"]

class BookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingStatus
        fields = ["status_name"]

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'

class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        