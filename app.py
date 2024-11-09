# api/index.py

from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Sample data
activity_footprint_factors = {
    "car": 0.21,
    "flight": 0.25,
    "train": 0.1
}

# Test route to verify API is working
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "alive",
        "message": "Carbon Footprint Calculator API is running"
    })

# Health check route
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/v1/calculate', methods=['POST', 'OPTIONS'])
def calculate_footprint():
    # Handle OPTIONS request for CORS preflight
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        data = request.get_json()

        # Log incoming request data (helpful for debugging)
        print("Received data:", data)

        activity = data.get("activity")
        amount = data.get("amount")

        if not activity or amount is None:
            return jsonify({"error": "Please provide both activity and amount."}), 400

        factor = activity_footprint_factors.get(activity.lower())
        if factor is None:
            return jsonify({"error": f"Activity '{activity}' is not recognized."}), 400

        footprint = factor * amount

        recommendation = (
            "Consider reducing your usage of this activity." if footprint > 10 else
            "Your carbon footprint for this activity is relatively low."
        )

        response = jsonify({
            "activity": activity,
            "amount": amount,
            "footprint": round(footprint, 2),
            "recommendation": recommendation
        })

        # Explicitly add CORS headers to response
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except Exception as e:
        print("Error:", str(e))  # Log the error
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500