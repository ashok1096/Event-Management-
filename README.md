# EventPulse Backend API

Conference and Multi-Session Event Management Portal - Backend API built with FastAPI.

## Features

- **Event Management**: Create, list, update, and manage events
- **Registration System**: Attendee registration with unique codes
- **Session Management**: Multi-session events with speaker assignments
- **Check-in System**: Event and session check-in with code-based verification
- **Feedback Collection**: Capture and analyze attendee feedback
- **Speaker Management**: Manage speaker profiles and session assignments
- **Analytics & Reporting**: Event statistics and engagement metrics
- **Audit Logging**: MongoDB-based activity and audit trails
- **Multi-database**: PostgreSQL for primary data, MongoDB for analytics

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── database/            # Database connections (PostgreSQL & MongoDB)
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic models for validation
│   ├── routers/             # API endpoint routes
│   ├── services/            # Business logic services
│   └── utils/               # Helper functions
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Installation

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- MongoDB 4.4+ (optional, for analytics)

### Setup

1. **Clone and navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # or
   source venv/bin/activate      # On Linux/Mac
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Create database**:
   ```bash
   # Create PostgreSQL database
   psql -U postgres -c "CREATE DATABASE eventpulse;"
   ```

## Running the Application

### Development Server

```bash
python -m uvicorn backend.app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Production Server

```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## Available Endpoints

### Events
- `POST /events/` - Create event
- `GET /events/` - List events
- `GET /events/{event_id}` - Get event details
- `PUT /events/{event_id}` - Update event
- `DELETE /events/{event_id}` - Delete event
- `GET /events/{event_id}/stats` - Get event statistics

### Registrations
- `POST /registrations/` - Register attendee
- `GET /registrations/{registration_id}` - Get registration details
- `GET /registrations/event/{event_id}` - List event registrations
- `PUT /registrations/{registration_id}` - Update registration
- `POST /registrations/{registration_id}/check-in` - Check-in attendee
- `DELETE /registrations/{registration_id}/cancel` - Cancel registration

### Sessions
- `POST /sessions/` - Create session
- `GET /sessions/` - List sessions
- `GET /sessions/{session_id}` - Get session details
- `PUT /sessions/{session_id}` - Update session
- `POST /sessions/{session_id}/start` - Start session
- `POST /sessions/{session_id}/end` - End session

### Check-ins
- `POST /checkins/registration-checkin` - Check-in with registration code
- `POST /checkins/session-checkin` - Check-in to session
- `GET /checkins/event/{event_id}/stats` - Event check-in statistics

### Speakers
- `POST /speakers/` - Create speaker profile
- `GET /speakers/` - List speakers
- `GET /speakers/{speaker_id}` - Get speaker details
- `PUT /speakers/{speaker_id}` - Update speaker
- `GET /speakers/{speaker_id}/sessions` - Get speaker sessions

### Feedback
- `POST /feedback/` - Submit feedback
- `GET /feedback/{feedback_id}` - Get feedback
- `GET /feedback/session/{session_id}` - List session feedback
- `GET /feedback/event/{event_id}` - List event feedback
- `GET /feedback/session/{session_id}/stats` - Session feedback statistics
- `GET /feedback/event/{event_id}/stats` - Event feedback statistics

## Database Models

### Event
```python
- id: Integer (Primary Key)
- title: String (Required)
- description: Text
- location: String
- start_date: DateTime (Required)
- end_date: DateTime (Required)
- max_attendees: Integer
- current_attendees: Integer
- status: String (upcoming, ongoing, completed, cancelled)
- organizer: String
- created_at: DateTime
- updated_at: DateTime
- is_active: Boolean
```

### Registration
```python
- id: Integer (Primary Key)
- event_id: Integer (Foreign Key)
- attendee_name: String (Required)
- attendee_email: String (Required)
- phone: String
- company: String
- registration_code: String (Unique)
- status: String
- is_checked_in: Boolean
- checked_in_at: DateTime
- payment_status: String
- created_at: DateTime
- updated_at: DateTime
```

### Session
```python
- id: Integer (Primary Key)
- event_id: Integer (Foreign Key)
- speaker_id: Integer (Foreign Key)
- title: String (Required)
- description: Text
- start_time: DateTime (Required)
- end_time: DateTime (Required)
- location: String
- capacity: Integer
- current_attendees: Integer
- session_code: String (Unique)
- status: String
- created_at: DateTime
- updated_at: DateTime
```

### CheckIn
```python
- id: Integer (Primary Key)
- registration_id: Integer (Foreign Key)
- session_id: Integer (Foreign Key)
- checkin_type: String
- timestamp: DateTime
- location: String
- device_id: String
```

### Feedback
```python
- id: Integer (Primary Key)
- event_id: Integer (Foreign Key)
- session_id: Integer (Foreign Key)
- registration_id: Integer (Foreign Key)
- rating: Integer (1-5)
- comment: Text
- created_at: DateTime
- updated_at: DateTime
```

### Speaker
```python
- id: Integer (Primary Key)
- name: String (Required)
- email: String (Unique, Required)
- bio: Text
- company: String
- expertise: String
- profile_url: String
- created_at: DateTime
- updated_at: DateTime
- is_active: Boolean
```

## Environment Variables

See `.env.example` for all available configuration options:

- `DATABASE_URL` - PostgreSQL connection string
- `MONGO_URL` - MongoDB connection string
- `SECRET_KEY` - JWT secret key for authentication
- `LOG_LEVEL` - Logging level (INFO, DEBUG, ERROR)
- `CORS_ORIGINS` - Allowed CORS origins

## Testing

Run the test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=backend/app
```

## Development

### Code Quality

Format code with black:
```bash
black backend/
```

Lint with flake8:
```bash
flake8 backend/
```

Type checking with mypy:
```bash
mypy backend/
```

## Deployment

### Docker

Build Docker image:
```bash
docker build -t eventpulse-backend .
```

Run container:
```bash
docker run -p 8000:8000 --env-file .env eventpulse-backend
```

### Docker Compose

```bash
docker-compose up -d
```

## API Response Format

All endpoints follow a consistent response format:

**Success Response**:
```json
{
  "id": 1,
  "title": "Annual Conference 2024",
  "status": "upcoming",
  ...
}
```

**Error Response**:
```json
{
  "detail": "Error message describing what went wrong"
}
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

## License

MIT License

## Support

For issues and questions, please contact the EventPulse team.
