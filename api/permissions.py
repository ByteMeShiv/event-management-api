from rest_framework import permissions

class IsOrganizerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow organizers of an event to edit or delete it.
    Read-only access is allowed for everyone else.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions (GET, HEAD, OPTIONS) are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the organizer of the event
        return obj.organizer == request.user

class IsRSVPOwner(permissions.BasePermission):
    """
    Custom permission to only allow the user who made the RSVP to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Only the user associated with the RSVP can edit or delete it
        return obj.user == request.user