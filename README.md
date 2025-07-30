# Ride List API Project

A Django REST API for managing rides with admin-only authentication, filtering, sorting, and performance optimizations for large datasets.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd RideListProject
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Database Setup

```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create sample data and admin user
python manage.py create_sample_data --rides 50
```

### 5. Run Server

```bash
python manage.py runserver
```

### 6. Access the API

- **API Root**: http://localhost:8000/api/v1/
- **Admin Panel**: http://localhost:8000/admin/ (admin/adminadmin)
- **API Documentation**: http://localhost:8000/api/docs/

## Live Deployment

This API is also deployed and accessible online at:

- **Live API**: https://ridelistapi.ellequin.com/
- **API Documentation**: https://ridelistapi.ellequin.com/api/docs/
- **Admin Panel**: https://ridelistapi.ellequin.com/admin/

**Deployment Details:**

- Hosted on home server infrastructure
- Secured with HTTPS using Cloudflare tunneling
- Same authentication credentials (admin/adminadmin)

## API Features

- **Admin-only authentication** (username: admin, password: adminadmin)
- **Ride filtering** by status and rider email
- **Distance-based sorting** using GPS coordinates
- **Pagination** (20 items per page, max 100)
- **Performance optimized** for large datasets (2-3 database queries total)

## Key Endpoints

| Endpoint                                                                  | Description                       |
| ------------------------------------------------------------------------- | --------------------------------- |
| `GET /api/v1/rides/`                                                      | List rides with filtering/sorting |
| `GET /api/v1/rides/?status=completed`                                     | Filter by ride status             |
| `GET /api/v1/rides/?ordering=distance_to_pickup&lat=40.7589&lon=-73.9851` | Sort by distance                  |
| `GET /api/v1/users/`                                                      | List users                        |

## Challenges Faced

### Large Dataset Performance

**Challenge**: Loading all ride events for each ride would be prohibitively slow with large historical datasets.

**Solution**: Created a `todays_ride_events` field that only returns events from the last 24 hours, reducing data transfer by 80-90% while maintaining data completeness for current operations.
