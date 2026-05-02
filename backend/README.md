# Movie Booking System

A full-stack movie booking application built with FastAPI (backend) and React (frontend), featuring JWT authentication with role-based access control.

## Features

- User registration and login with JWT authentication
- Role-based access: Admin, Manager, User
- Movie management (CRUD operations)
- Booking system
- Responsive UI inspired by QuickShow design

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT for authentication
- Pydantic for data validation

### Frontend
- React with Vite
- React Router for navigation
- Axios for API calls
- CSS for styling

## API Endpoints

### Authentication
- POST /auth/register - Register a new user
- POST /auth/login - Login and get access token

### Movies
- GET /movies - Get all movies
- POST /movies - Create a new movie (admin only)

### Bookings
- GET /bookings - Get user's bookings
- POST /bookings - Create a new booking

## Setup Instructions

### Backend
1. Navigate to the backend directory:
   ```
   cd backend
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the server:
   ```
   uvicorn app.main:app --reload
   ```

### Frontend
1. Navigate to the frontend directory:
   ```
   cd frontend
   ```
2. Install dependencies:
   ```
   npm install
   ```
3. Run the development server:
   ```
   npm run dev
   ```

## Database

The application uses PostgreSQL as the primary database.

Default local connection:
`postgresql+psycopg2://movie_user:movie_password@db:5432/movie_booking`

When you run the stack with Docker Compose, the `db` service provides this database automatically.

## Default Admin

On backend startup, the project creates a default admin account automatically if it does not exist.

- Email: `admin@quickshow.local`
- Password: `AdminPass123!`

You can override these values in `backend/.env` with:

- `DEFAULT_ADMIN_EMAIL`
- `DEFAULT_ADMIN_PASSWORD`

## Testing

Basic testing can be added using pytest for backend and Jest for frontend.

## Team Members

- Developer: [Your Name]

## Demo

To run the full system:
1. Start the backend server
2. Start the frontend development server
3. Open http://localhost:3000 in your browser
