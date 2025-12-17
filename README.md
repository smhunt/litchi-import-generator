# Litchi Import Generator

A Python Flask API for generating Litchi-compatible mission CSV files. This tool allows you to programmatically create drone mission files for the Litchi flight planning app.

## Features

- **Flask REST API** for generating Litchi CSV mission files
- **Input validation** for waypoint parameters
- **Example missions** including a pre-configured route for Ilderton, Ontario
- **CORS support** for web-based clients
- **Litchi CSV format compliance** with all standard fields

## Installation

1. Clone the repository:
```bash
git clone https://github.com/smhunt/litchi-import-generator.git
cd litchi-import-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Server

Run the Flask development server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### API Endpoints

#### Health Check
```bash
GET /health
```

Returns the health status of the API.

#### Generate Mission CSV
```bash
POST /api/generate-mission
Content-Type: application/json
```

Generate a custom Litchi mission CSV file from waypoint data.

**Request Body Example:**
```json
{
  "mission_name": "my_mission",
  "waypoints": [
    {
      "latitude": 43.0347,
      "longitude": -81.2453,
      "altitude": 50.0,
      "heading": 0,
      "curve_size": 0,
      "rotation_direction": 0,
      "gimbal_mode": 0,
      "gimbal_pitch_angle": -90,
      "action_type_1": -1,
      "action_param_1": 0
    }
  ]
}
```

**Response:** CSV file download

#### Example Mission - Ilderton, Ontario
```bash
GET /api/example-mission/ilderton
```

Downloads a pre-configured square pattern mission around Ilderton, Ontario.

### Using cURL

**Generate a custom mission:**
```bash
curl -X POST http://localhost:5000/api/generate-mission \
  -H "Content-Type: application/json" \
  -d '{
    "mission_name": "test_mission",
    "waypoints": [
      {
        "latitude": 43.0347,
        "longitude": -81.2453,
        "altitude": 50.0,
        "heading": 0,
        "gimbal_pitch_angle": -90
      }
    ]
  }' \
  --output mission.csv
```

**Get the Ilderton example mission:**
```bash
curl http://localhost:5000/api/example-mission/ilderton --output ilderton_mission.csv
```

## Waypoint Parameters

### Required Fields
- `latitude`: Latitude in degrees (-90 to 90)
- `longitude`: Longitude in degrees (-180 to 180)
- `altitude`: Altitude in meters (non-negative)

### Optional Fields
- `heading`: Heading in degrees (-180 to 360), default: 0
- `curve_size`: Curve size in meters, default: 0
- `rotation_direction`: Rotation direction (0, 1, or 2), default: 0
- `gimbal_mode`: Gimbal mode, default: 0
- `gimbal_pitch_angle`: Gimbal pitch angle in degrees (-90 to 30), default: -90
- `action_type_1` through `action_type_15`: Action types, default: -1
- `action_param_1` through `action_param_15`: Action parameters, default: 0
- `altitude_mode`: Altitude mode, default: 0
- `speed`: Speed in m/s, default: 0
- `poi_latitude`, `poi_longitude`, `poi_altitude`: Point of Interest coordinates
- `photo_time_interval`: Photo time interval, default: -1
- `photo_dist_interval`: Photo distance interval, default: -1

## Litchi CSV Format

The generated CSV files follow the official Litchi mission format specification with the following columns:

- latitude, longitude, altitude(m)
- heading(deg), curvesize(m), rotationdir
- gimbalmode, gimbalpitchangle
- actiontype1-15, actionparam1-15
- altitudemode, speed(m/s)
- poi_latitude, poi_longitude, poi_altitude(m), poi_altitudemode
- photo_timeinterval, photo_distinterval

## Development

### Project Structure
```
litchi-import-generator/
├── app.py                    # Flask API application
├── litchi_csv_generator.py   # CSV generation module
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore file
└── README.md                # This file
```

### Running Tests

Test the API manually using the health check and example endpoints:
```bash
# Check if the server is running
curl http://localhost:5000/health

# Download the example mission
curl http://localhost:5000/api/example-mission/ilderton --output test.csv
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available for experimentation with generating Litchi mission files.
