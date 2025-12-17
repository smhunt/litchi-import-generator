"""
Litchi Mission CSV Generator API
A Flask API for generating Litchi-compatible mission CSV files
"""
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from litchi_csv_generator import generate_litchi_csv, validate_waypoint

app = Flask(__name__)
CORS(app)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Litchi CSV Generator API is running"})


@app.route('/api/generate-mission', methods=['POST'])
def generate_mission():
    """
    Generate a Litchi mission CSV file from waypoint data
    
    Expected JSON format:
    {
        "mission_name": "My Mission",
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
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        mission_name = data.get('mission_name', 'mission')
        waypoints = data.get('waypoints', [])
        
        if not waypoints:
            return jsonify({"error": "No waypoints provided"}), 400
        
        # Validate waypoints
        for idx, waypoint in enumerate(waypoints):
            is_valid, error_msg = validate_waypoint(waypoint)
            if not is_valid:
                return jsonify({"error": f"Waypoint {idx}: {error_msg}"}), 400
        
        # Generate CSV
        csv_content = generate_litchi_csv(waypoints)
        
        # Create response with CSV file
        response = make_response(csv_content)
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename={mission_name}.csv'
        
        return response
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/example-mission/ilderton', methods=['GET'])
def example_ilderton_mission():
    """
    Get an example mission for Ilderton, Ontario
    This creates a simple square pattern mission around Ilderton
    """
    # Ilderton, Ontario coordinates: approximately 43.0347° N, 81.2453° W
    waypoints = [
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
        },
        {
            "latitude": 43.0357,
            "longitude": -81.2453,
            "altitude": 50.0,
            "heading": 90,
            "curve_size": 0,
            "rotation_direction": 0,
            "gimbal_mode": 0,
            "gimbal_pitch_angle": -90,
            "action_type_1": -1,
            "action_param_1": 0
        },
        {
            "latitude": 43.0357,
            "longitude": -81.2443,
            "altitude": 50.0,
            "heading": 180,
            "curve_size": 0,
            "rotation_direction": 0,
            "gimbal_mode": 0,
            "gimbal_pitch_angle": -90,
            "action_type_1": -1,
            "action_param_1": 0
        },
        {
            "latitude": 43.0347,
            "longitude": -81.2443,
            "altitude": 50.0,
            "heading": 270,
            "curve_size": 0,
            "rotation_direction": 0,
            "gimbal_mode": 0,
            "gimbal_pitch_angle": -90,
            "action_type_1": -1,
            "action_param_1": 0
        }
    ]
    
    csv_content = generate_litchi_csv(waypoints)
    
    response = make_response(csv_content)
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=ilderton_mission.csv'
    
    return response


if __name__ == '__main__':
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
