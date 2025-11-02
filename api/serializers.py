from rest_framework import serializers
from .models import UserProfile, Event, RSVP, Review

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'full_name', 'bio', 'location']

class ReviewSerializer(serializers.ModelSerializer):
    # Show the username, not just the user ID
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user']

class RSVPSerializer(serializers.ModelSerializer):
    # Show the username, not just the user ID
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = RSVP
        fields = ['id', 'user', 'status']
        read_only_fields = ['user']

class EventSerializer(serializers.ModelSerializer):
    # Use the username for the organizer field
    organizer = serializers.ReadOnlyField(source='organizer.username')
    # Nest reviews directly in the event detail
    reviews = ReviewSerializer(many=True, read_only=True)
    # Count RSVPs
    rsvps_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'organizer', 'location', 
            'start_time', 'end_time', 'is_public', 
            'rsvps_count', 'reviews'
        ]
        read_only_fields = ['organizer', 'reviews', 'rsvps_count']
    
    def get_rsvps_count(self, obj):
        # Get a count of all RSVPs for this event
        return obj.rsvps.count()