from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from django.db.models import Q
from .models import Event, Review, RSVP, UserProfile
from .serializers import EventSerializer, ReviewSerializer, RSVPSerializer
from .permissions import IsOrganizerOrReadOnly, IsRSVPOwner

# 1. Event API
class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed, created, edited, or deleted.
    """
    serializer_class = EventSerializer
    # Use custom permission: Must be authenticated, but only organizer can edit/delete
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly]

    def get_queryset(self):
        """
        This view should return a list of all public events
        or private events owned by the current user.
        """
        user = self.request.user
        if user.is_authenticated:
            # Show public events OR private events where the user is the organizer
            return Event.objects.filter(
                Q(is_public=True) | Q(organizer=user)
            ).distinct()
        
        # For unauthenticated users, only show public events
        return Event.objects.filter(is_public=True)

    def perform_create(self, serializer):
        """
        Automatically set the logged-in user as the organizer.
        """
        serializer.save(organizer=self.request.user)

# 2. Review API (Nested under Events)
class ReviewListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating reviews for a specific event.
    """
    serializer_class = ReviewSerializer
    # Allow any authenticated user to list or create (post) a review
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Return all reviews for the event ID in the URL.
        """
        event_id = self.kwargs['event_id']
        return Review.objects.filter(event_id=event_id)

    def perform_create(self, serializer):
        """
        Automatically set the event (from URL) and user (from request).
        """
        event = get_object_or_404(Event, id=self.kwargs['event_id'])
        
        # Check if user already reviewed
        if Review.objects.filter(event=event, user=self.request.user).exists():
            raise serializers.ValidationError("You have already reviewed this event.")
            
        serializer.save(user=self.request.user, event=event)

# 3. RSVP API (Nested under Events)
class RSVPListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing all RSVPs for an event and creating one.
    """
    serializer_class = RSVPSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Return all RSVPs for the event ID in the URL.
        """
        event_id = self.kwargs['event_id']
        return RSVP.objects.filter(event_id=event_id)

    def perform_create(self, serializer):
        """
        Automatically set the event (from URL) and user (from request).
        """
        event = get_object_or_404(Event, id=self.kwargs['event_id'])
        
        # Check if user already RSVP'd
        if RSVP.objects.filter(event=event, user=self.request.user).exists():
            raise serializers.ValidationError("You have already RSVP'd to this event. Use PATCH to update.")
            
        serializer.save(user=self.request.user, event=event)

class RSVPDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for updating (PATCH) or deleting (DELETE) a specific RSVP.
    """
    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer
    permission_classes = [IsRSVPOwner] # Only the RSVP owner can change it
    lookup_url_kwarg = 'rsvp_id' # To find the RSVP by its ID from the URL

    def get_queryset(self):
        """
        Ensure the user can only access their own RSVPs for the given event.
        """
        event_id = self.kwargs['event_id']
        return RSVP.objects.filter(event_id=event_id, user=self.request.user)