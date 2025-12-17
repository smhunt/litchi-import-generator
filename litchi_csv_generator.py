"""
Litchi CSV Generator Module
Generates CSV files in Litchi mission format
"""
import csv
import io


# Litchi CSV column headers based on Litchi mission format specification
LITCHI_HEADERS = [
    'latitude',
    'longitude',
    'altitude(m)',
    'heading(deg)',
    'curvesize(m)',
    'rotationdir',
    'gimbalmode',
    'gimbalpitchangle',
    'actiontype1',
    'actionparam1',
    'actiontype2',
    'actionparam2',
    'actiontype3',
    'actionparam3',
    'actiontype4',
    'actionparam4',
    'actiontype5',
    'actionparam5',
    'actiontype6',
    'actionparam6',
    'actiontype7',
    'actionparam7',
    'actiontype8',
    'actionparam8',
    'actiontype9',
    'actionparam9',
    'actiontype10',
    'actionparam10',
    'actiontype11',
    'actionparam11',
    'actiontype12',
    'actionparam12',
    'actiontype13',
    'actionparam13',
    'actiontype14',
    'actionparam14',
    'actiontype15',
    'actionparam15',
    'altitudemode',
    'speed(m/s)',
    'poi_latitude',
    'poi_longitude',
    'poi_altitude(m)',
    'poi_altitudemode',
    'photo_timeinterval',
    'photo_distinterval'
]


def validate_waypoint(waypoint):
    """
    Validate a waypoint dictionary
    
    Args:
        waypoint (dict): Waypoint data
        
    Returns:
        tuple: (is_valid, error_message)
    """
    required_fields = ['latitude', 'longitude', 'altitude']
    
    for field in required_fields:
        if field not in waypoint:
            return False, f"Missing required field: {field}"
    
    # Validate latitude range
    lat = waypoint.get('latitude')
    try:
        lat = float(lat)
        if lat < -90 or lat > 90:
            return False, f"Latitude must be between -90 and 90, got {lat}"
    except (TypeError, ValueError):
        return False, f"Latitude must be a number, got {lat}"
    
    # Validate longitude range
    lon = waypoint.get('longitude')
    try:
        lon = float(lon)
        if lon < -180 or lon > 180:
            return False, f"Longitude must be between -180 and 180, got {lon}"
    except (TypeError, ValueError):
        return False, f"Longitude must be a number, got {lon}"
    
    # Validate altitude
    alt = waypoint.get('altitude')
    try:
        alt = float(alt)
        if alt < 0:
            return False, f"Altitude must be non-negative, got {alt}"
    except (TypeError, ValueError):
        return False, f"Altitude must be a number, got {alt}"
    
    # Validate heading if provided
    if 'heading' in waypoint:
        heading = waypoint.get('heading')
        try:
            heading = float(heading)
            if heading < -180 or heading > 360:
                return False, f"Heading must be between -180 and 360, got {heading}"
        except (TypeError, ValueError):
            return False, f"Heading must be a number, got {heading}"
    
    # Validate gimbal pitch angle if provided
    if 'gimbal_pitch_angle' in waypoint:
        gimbal = waypoint.get('gimbal_pitch_angle')
        try:
            gimbal = float(gimbal)
            if gimbal < -90 or gimbal > 30:
                return False, f"Gimbal pitch angle must be between -90 and 30, got {gimbal}"
        except (TypeError, ValueError):
            return False, f"Gimbal pitch angle must be a number, got {gimbal}"
    
    return True, ""


def generate_litchi_csv(waypoints):
    """
    Generate a Litchi CSV file content from waypoint data
    
    Args:
        waypoints (list): List of waypoint dictionaries
        
    Returns:
        str: CSV content as string
    """
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=LITCHI_HEADERS)
    
    # Write header
    writer.writeheader()
    
    # Write waypoints
    for waypoint in waypoints:
        row = {}
        
        # Map input fields to Litchi CSV format
        row['latitude'] = waypoint.get('latitude', 0)
        row['longitude'] = waypoint.get('longitude', 0)
        row['altitude(m)'] = waypoint.get('altitude', 50)
        row['heading(deg)'] = waypoint.get('heading', 0)
        row['curvesize(m)'] = waypoint.get('curve_size', 0)
        row['rotationdir'] = waypoint.get('rotation_direction', 0)
        row['gimbalmode'] = waypoint.get('gimbal_mode', 0)
        row['gimbalpitchangle'] = waypoint.get('gimbal_pitch_angle', -90)
        
        # Action parameters (up to 15 actions)
        for i in range(1, 16):
            action_type_key = f'action_type_{i}'
            action_param_key = f'action_param_{i}'
            row[f'actiontype{i}'] = waypoint.get(action_type_key, -1)
            row[f'actionparam{i}'] = waypoint.get(action_param_key, 0)
        
        # Optional parameters with defaults
        row['altitudemode'] = waypoint.get('altitude_mode', 0)
        row['speed(m/s)'] = waypoint.get('speed', 0)
        row['poi_latitude'] = waypoint.get('poi_latitude', 0)
        row['poi_longitude'] = waypoint.get('poi_longitude', 0)
        row['poi_altitude(m)'] = waypoint.get('poi_altitude', 0)
        row['poi_altitudemode'] = waypoint.get('poi_altitude_mode', 0)
        row['photo_timeinterval'] = waypoint.get('photo_time_interval', -1)
        row['photo_distinterval'] = waypoint.get('photo_dist_interval', -1)
        
        writer.writerow(row)
    
    csv_content = output.getvalue()
    output.close()
    
    return csv_content
