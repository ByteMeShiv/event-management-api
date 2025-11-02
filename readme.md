# Event Management System API

This is a RESTful API for managing events, built with Django and Django REST Framework.

## Features Implemented (24-Hour Task)

Given the 24-hour timeframe, I prioritized the core, foundational features of the API.

* **Models:** All 4 models (`UserProfile`, `Event`, `RSVP`, `Review`) with correct relationships.
* **JWT Authentication:** Secure user authentication using `djangorestframework-simplejwt`.
* **Event API:** Full CRUD operations for Events (`/api/events/`).
* **Core Permissions:**
    * Only authenticated users can create events.
    * Only the **organizer** of an event can edit or delete it (via `IsOrganizerOrReadOnly` permission).
* **Public/Private Events:** The main event list (`/api/events/`) only shows public events or private events organized by the logged-in user.
* **Pagination:** All list endpoints are paginated.
* **Review API:** Users can `POST` reviews and `GET` a list of reviews for a specific event.
* **RSVP API:** Users can `POST` an RSVP for an event and `PATCH` their RSVP status.

## Setup & Installation

1.  Clone the repository:
    `git clone https://github.com/your-username/event-management-system.git`
2.  Navigate to the directory:
    `cd event-management-system`
3.  Create and activate a virtual environment:
    `python -m venv venv`
    `source venv/bin/activate`
4.  Install dependencies:
    `pip install -r requirements.txt`
5.  Run database migrations:
    `python manage.py migrate`
6.  Run the server:
    `python manage.py runserver`

## API Endpoints

### Auth
* `POST /api/token/` (Get JWT token)
* `POST /api/token/refresh/`

### Events
* `POST /api/events/` (Create Event)
* `GET /api/events/` (List public/my events)
* `GET /api/events/{id}/` (Get event details)
* `PUT /api/events/{id}/` (Update event - *Organizer only*)
* `DELETE /api/events/{id}/` (Delete event - *Organizer only*)

### Reviews
* `POST /api/events/{event_id}/reviews/` (Add review)
* `GET /api/events/{event_id}/reviews/` (List reviews)

### RSVPs
* `POST /api/events/{event_id}/rsvp/` (RSVP to event)
* `GET /api/events/{event_id}/rsvp/` (List RSVPs for an event)
* `PATCH /api/events/{event_id}/rsvp/{rsvp_id}/` (Update RSVP status - *Owner only*)

---
*Files like `manage.py` and `db.sqlite3` are auto-generated and need no changes.*
---