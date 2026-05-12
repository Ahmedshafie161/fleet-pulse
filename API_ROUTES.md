# FleetPulse API Routes Documentation

Complete reference for all REST API endpoints with examples and usage.

---

## Authentication

### Login
**POST** `/api/v1/auth/login`

Obtain JWT token for authenticated requests.

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -d "username=admin&password=admin1234"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Header for subsequent requests:**
```bash
Authorization: Bearer <access_token>
```

---

## Users

### Create User
**POST** `/api/v1/users`

Create a new user account. No authentication required.

**Request Body:**
```json
{
  "username": "sarah_johnson",
  "password": "SecurePass123"
}
```

**Response:** 201 Created
```json
{
  "id": 2,
  "username": "sarah_johnson",
  "created_at": "2026-05-12T09:30:00Z"
}
```

**Validation:**
- Username must be unique
- Password must be at least 8 characters

### List Users
**GET** `/api/v1/users`

List all users in the system. Requires authentication.

**Response:**
```json
[
  {
    "id": 1,
    "username": "admin",
    "created_at": "2026-05-12T08:30:00Z"
  },
  {
    "id": 2,
    "username": "sarah_johnson",
    "created_at": "2026-05-12T09:30:00Z"
  }
]
```

### Change Password
**POST** `/api/v1/users/password`

Change the current user's password. Requires authentication.

**Request Body:**
```json
{
  "old_password": "admin1234",
  "new_password": "newpassword123"
}
```

**Response:** 204 No Content

**Validation:**
- Old password must be correct
- New password must be at least 8 characters

---

## Vehicles

### List Vehicles
**GET** `/api/v1/vehicles`

List all vehicles with pagination support.

**Query Parameters:**
- `skip` (int, default: 0) - Number of records to skip
- `limit` (int, default: 100) - Number of records to return

**Response:**
```json
[
  {
    "id": 1,
    "vin": "1G1FB1C30D1234567",
    "plate": "FL001",
    "make": "Chevrolet",
    "model": "Silverado",
    "year": 2021,
    "fuel_type": "diesel",
    "odometer_km": 15000.0,
    "is_active": true,
    "firmware_version": "v2.1.0",
    "created_at": "2026-05-12T08:30:00Z",
    "updated_at": "2026-05-12T08:30:00Z"
  }
]
```

### Get Vehicle Details
**GET** `/api/v1/vehicles/{vehicle_id}`

Get detailed information about a specific vehicle.

**Response:**
```json
{
  "id": 1,
  "vin": "1G1FB1C30D1234567",
  "plate": "FL001",
  "make": "Chevrolet",
  "model": "Silverado",
  "year": 2021,
  "fuel_type": "diesel",
  "odometer_km": 15000.0,
  "is_active": true,
  "firmware_version": "v2.1.0",
  "created_at": "2026-05-12T08:30:00Z",
  "updated_at": "2026-05-12T08:30:00Z"
}
```

### Create Vehicle
**POST** `/api/v1/vehicles`

Create a new vehicle. VIN must be unique.

**Request Body:**
```json
{
  "vin": "5TDJKRFH2LS123456",
  "plate": "FL005",
  "make": "Lexus",
  "model": "RX 350",
  "year": 2024,
  "fuel_type": "hybrid"
}
```

**Response:** 201 Created

### Update Vehicle
**PATCH** `/api/v1/vehicles/{vehicle_id}`

Update vehicle information.

**Request Body:**
```json
{
  "plate": "FL005_NEW",
  "odometer_km": 20000.0,
  "is_active": false
}
```

**Response:** 200 OK (updated vehicle object)

### Delete Vehicle
**DELETE** `/api/v1/vehicles/{vehicle_id}`

Delete a vehicle permanently.

**Response:** 204 No Content

---

## Drivers

### List Drivers
**GET** `/api/v1/drivers`

List all drivers.

**Response:**
```json
[
  {
    "id": 1,
    "first_name": "John",
    "last_name": "Smith",
    "license_number": "DL1234567",
    "license_expiry": "2027-05-12T00:00:00Z",
    "phone": "555-0101",
    "email": "john.smith@example.com",
    "is_active": true,
    "assigned_vehicle_id": 1,
    "created_at": "2026-05-12T08:30:00Z",
    "updated_at": "2026-05-12T08:30:00Z"
  }
]
```

### Get Driver Details
**GET** `/api/v1/drivers/{driver_id}`

Get detailed information about a specific driver.

**Response:** Driver object (see List Drivers)

### Create Driver
**POST** `/api/v1/drivers`

Create a new driver. License number must be unique.

**Request Body:**
```json
{
  "first_name": "Sarah",
  "last_name": "Johnson",
  "license_number": "DL1234570",
  "license_expiry": "2027-12-31",
  "phone": "555-0104",
  "email": "sarah.johnson@example.com",
  "assigned_vehicle_id": 2
}
```

**Response:** 201 Created

### Update Driver
**PATCH** `/api/v1/drivers/{driver_id}`

Update driver information.

**Request Body:**
```json
{
  "phone": "555-0105",
  "assigned_vehicle_id": 3,
  "is_active": false
}
```

**Response:** 200 OK (updated driver object)

### Delete Driver
**DELETE** `/api/v1/drivers/{driver_id}`

Delete a driver permanently.

**Response:** 204 No Content

---

## Trips

### List Trips
**GET** `/api/v1/trips`

List all trips with optional filtering.

**Query Parameters:**
- `vehicle_id` (int, optional) - Filter by vehicle
- `status` (string, optional) - Filter by status (in_progress, completed)

**Response:**
```json
[
  {
    "id": 1,
    "vehicle_id": 1,
    "driver_id": 1,
    "started_at": "2026-05-12T06:30:00Z",
    "ended_at": "2026-05-12T07:30:00Z",
    "start_lat": 37.7749,
    "start_lng": -122.4194,
    "end_lat": 37.8044,
    "end_lng": -122.2712,
    "distance_km": 50.0,
    "max_speed_kmh": 85.0,
    "avg_speed_kmh": 65.0,
    "fuel_consumed_l": 5.5,
    "status": "completed",
    "created_at": "2026-05-12T08:30:00Z"
  }
]
```

### Get Trip Details
**GET** `/api/v1/trips/{trip_id}`

Get detailed information about a specific trip.

**Response:** Trip object (see List Trips)

### Create Trip
**POST** `/api/v1/trips`

Start a new trip.

**Request Body:**
```json
{
  "vehicle_id": 1,
  "driver_id": 1
}
```

**Response:** 201 Created (Trip object with `status: "in_progress"`)

### Update Trip
**PATCH** `/api/v1/trips/{trip_id}`

Update trip information (typically to end a trip).

**Request Body:**
```json
{
  "ended_at": "2026-05-12T09:30:00Z",
  "distance_km": 55.5,
  "avg_speed_kmh": 68.0,
  "fuel_consumed_l": 6.0,
  "status": "completed"
}
```

**Response:** 200 OK (updated trip object)

---

## Telemetry

### List Telemetry
**GET** `/api/v1/telemetry`

List telemetry records with filtering options.

**Query Parameters:**
- `vehicle_id` (int, optional) - Filter by vehicle
- `trip_id` (int, optional) - Filter by trip
- `skip` (int, default: 0) - Pagination offset
- `limit` (int, default: 100) - Pagination limit

**Response:**
```json
[
  {
    "id": 1,
    "vehicle_id": 1,
    "trip_id": 1,
    "recorded_at": "2026-05-12T09:00:00Z",
    "latitude": 37.7749,
    "longitude": -122.4194,
    "speed_kmh": 45.0,
    "heading_deg": 180.0,
    "altitude_m": 10.0,
    "odometer_km": 15000.0,
    "fuel_level_pct": 75.0,
    "engine_rpm": 1500,
    "ignition": "ON",
    "source": "gps"
  }
]
```

### Create Telemetry Record
**POST** `/api/v1/telemetry`

Ingest a new telemetry data point (typically from GPS device).

**Request Body:**
```json
{
  "vehicle_id": 1,
  "trip_id": 1,
  "latitude": 37.7760,
  "longitude": -122.4180,
  "speed_kmh": 55.0,
  "heading_deg": 185.0,
  "altitude_m": 12.0,
  "odometer_km": 15010.0,
  "fuel_level_pct": 72.0,
  "engine_rpm": 1600,
  "ignition": "ON",
  "source": "gps"
}
```

**Response:** 201 Created

---

## Alerts

### List Alerts
**GET** `/api/v1/alerts`

List all alerts with optional filtering.

**Query Parameters:**
- `vehicle_id` (int, optional) - Filter by vehicle
- `is_acknowledged` (bool, optional) - Filter by acknowledgment status

**Response:**
```json
[
  {
    "id": 1,
    "vehicle_id": 1,
    "driver_id": 1,
    "trip_id": null,
    "alert_type": "speeding",
    "severity": "warning",
    "message": "speeding detected on vehicle FL001",
    "latitude": 37.7749,
    "longitude": -122.4194,
    "is_acknowledged": false,
    "acknowledged_at": null,
    "triggered_at": "2026-05-12T08:30:00Z"
  }
]
```

### Create Alert
**POST** `/api/v1/alerts`

Create a new alert (typically triggered by backend monitoring).

**Request Body:**
```json
{
  "vehicle_id": 2,
  "driver_id": 2,
  "alert_type": "low_fuel",
  "severity": "critical",
  "message": "Fuel level below 15%",
  "latitude": 37.8000,
  "longitude": -122.4200
}
```

**Response:** 201 Created

### Acknowledge Alert
**POST** `/api/v1/alerts/{alert_id}/acknowledge`

Mark an alert as acknowledged by a user.

**Response:** 200 OK (updated alert with `is_acknowledged: true`)

---

## Maintenance

### List Maintenance Records
**GET** `/api/v1/maintenance`

List all maintenance records with filtering.

**Query Parameters:**
- `vehicle_id` (int, optional) - Filter by vehicle
- `status` (string, optional) - Filter by status (scheduled, completed)

**Response:**
```json
[
  {
    "id": 1,
    "vehicle_id": 1,
    "service_type": "Oil Change",
    "status": "completed",
    "scheduled_at": "2026-05-19T00:00:00Z",
    "completed_at": "2026-05-11T00:00:00Z",
    "odometer_at_service_km": 15000.0,
    "next_service_km": 25000.0,
    "next_service_date": "2026-06-11T00:00:00Z",
    "technician": "John Doe",
    "notes": "Oil Change for FL001",
    "cost_eur": 150.0,
    "created_at": "2026-05-12T08:30:00Z",
    "updated_at": "2026-05-12T08:30:00Z"
  }
]
```

### Create Maintenance Record
**POST** `/api/v1/maintenance`

Create a new maintenance record.

**Request Body:**
```json
{
  "vehicle_id": 3,
  "service_type": "Tire Rotation",
  "scheduled_at": "2026-05-20T10:00:00Z",
  "next_service_km": 35000.0,
  "next_service_date": "2026-08-12T00:00:00Z"
}
```

**Response:** 201 Created

### Update Maintenance Record
**PATCH** `/api/v1/maintenance/{record_id}`

Update maintenance record (mark as completed, add costs, etc).

**Request Body:**
```json
{
  "status": "completed",
  "completed_at": "2026-05-12T14:00:00Z",
  "technician": "Jane Smith",
  "cost_eur": 200.0
}
```

**Response:** 200 OK (updated maintenance object)

---

## Fleet Configuration

### List Configurations
**GET** `/api/v1/fleet-config`

List all fleet configurations.

**Response:**
```json
[
  {
    "id": 1,
    "reference_name": "default_config",
    "display_name": "Default Fleet Configuration",
    "is_active": true,
    "idle_alert_threshold_minutes": 15,
    "low_fuel_threshold_pct": 15.0,
    "speed_limit_kmh": 100.0,
    "created_at": "2026-05-12T08:30:00Z",
    "updated_at": "2026-05-12T08:30:00Z"
  }
]
```

### Get Active Configuration
**GET** `/api/v1/fleet-config/active`

Get the currently active fleet configuration.

**Response:** Fleet Config object (see List Configurations)

### Create Configuration
**POST** `/api/v1/fleet-config`

Create a new fleet configuration. Display name must be unique.

**Request Body:**
```json
{
  "reference_name": "high_speed_config",
  "display_name": "High Speed Fleet",
  "idle_alert_threshold_minutes": 20,
  "low_fuel_threshold_pct": 20.0,
  "speed_limit_kmh": 120.0
}
```

**Response:** 201 Created

### Activate Configuration
**POST** `/api/v1/fleet-config/{reference_name}/activate`

Activate a specific configuration (deactivates all others).

**Response:** 200 OK (activated config object)

### Delete Configuration
**DELETE** `/api/v1/fleet-config/{reference_name}`

Delete an inactive configuration. Cannot delete active configuration.

**Response:** 204 No Content

---

## Error Responses

All endpoints return appropriate HTTP status codes:

- **200** - OK (successful GET/PATCH)
- **201** - Created (successful POST)
- **204** - No Content (successful DELETE)
- **400** - Bad Request (invalid input)
- **401** - Unauthorized (missing/invalid token)
- **404** - Not Found (resource doesn't exist)
- **422** - Unprocessable Entity (validation error)
- **500** - Internal Server Error

### Error Response Format
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Common Patterns

### Authentication
All endpoints except `POST /api/v1/auth/login` require authentication:
```bash
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/vehicles
```

### Pagination
List endpoints support pagination via query parameters:
```bash
curl "http://localhost:8000/api/v1/vehicles?skip=10&limit=20"
```

### Filtering
Many list endpoints support filtering:
```bash
curl "http://localhost:8000/api/v1/alerts?vehicle_id=1&is_acknowledged=false"
curl "http://localhost:8000/api/v1/trips?status=in_progress"
```

### Timestamps
All timestamps are in UTC ISO 8601 format: `2026-05-12T08:30:00Z`

---

## Testing with cURL

### 1. Login and get token
```bash
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -d "username=admin&password=admin1234" | jq -r '.access_token')
```

### 2. Create a vehicle
```bash
curl -X POST http://localhost:8000/api/v1/vehicles \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "vin": "5TDJKRFH2LS123456",
    "plate": "FL005",
    "make": "Lexus",
    "model": "RX 350",
    "year": 2024,
    "fuel_type": "hybrid"
  }'
```

### 3. List all vehicles
```bash
curl -X GET http://localhost:8000/api/v1/vehicles \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Start a trip
```bash
curl -X POST http://localhost:8000/api/v1/trips \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "vehicle_id": 1,
    "driver_id": 1
  }'
```

---

## Interactive API Documentation

Visit these URLs while the server is running:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive testing and full schema documentation.
