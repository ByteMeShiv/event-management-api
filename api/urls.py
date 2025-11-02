from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# The router will automatically create the URLs for the Event ViewSet
# /api/events/
# /api/events/{id}/
router = DefaultRouter()
router.register(r'events', views.EventViewSet, basename='event')

urlpatterns = [
    # Add the router's URLs
    path('', include(router.urls)),
    
    # Nested URLs for Reviews
    path(
        'events/<int:event_id>/reviews/', 
        views.ReviewListCreateView.as_view(), 
        name='event-reviews'
    ),
    
    # Nested URLs for RSVPs
    path(
        'events/<int:event_id>/rsvp/', 
        views.RSVPListCreateView.as_view(), 
        name='event-rsvps'
    ),
    path(
        'events/<int:event_id>/rsvp/<int:rsvp_id>/', 
        views.RSVPDetailView.as_view(), 
        name='rsvp-detail'
    ),
]