import os
import sys
from flask import Flask, request, jsonify
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import os

# Developed By 𝐌𝐀𝐓𝐑𝐈𝐗 ( @VZR7X )

sys.path.insert(0, os.path.dirname(__file__))

# Rename 'app' to 'application' for WSGI compatibility
application = Flask(__name__)

@application.route('/validate', methods=['GET'])
def validate_phone_number():
    phone_number = request.args.get('number')
    
    if not phone_number:
        return jsonify({"success": False, "message": "Phone number is required."}), 400

    try:
        # Parse phone number with a default region (optional)
        parsed_number = phonenumbers.parse(phone_number, None)
        
        # Check if the number is valid
        if not phonenumbers.is_valid_number(parsed_number):
            return jsonify({"success": False, "message": "Invalid phone number."}), 400
        
        # Check if the number is possible
        if not phonenumbers.is_possible_number(parsed_number):
            return jsonify({"success": False, "message": "Impossible phone number."}), 400
        
        # Get carrier information
        # API example: http://127.0.0.1:5000/validate?number=%2B[YOUR_NUMBER]
        carrier_name = carrier.name_for_number(parsed_number, "en")
        region = geocoder.description_for_number(parsed_number, "en")
        time_zones = timezone.time_zones_for_number(parsed_number)
        
        return jsonify({
            "success": True,
            "message": "Valid phone number!",
            "carrier": carrier_name,
            "region": region,
            "time_zones": list(time_zones)
        })
    
    except phonenumbers.NumberParseException as e:
        return jsonify({"success": False, "message": "Invalid phone number format: " + str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    app.run(host='0.0.0.0', port=port, debug=True)
