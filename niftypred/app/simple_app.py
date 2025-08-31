from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'NIFTY Prediction API is running'})

@app.route('/api/test', methods=['GET'])
def test():
    """Test endpoint"""
    return jsonify({'status': 'success', 'message': 'API is working!'})

@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({'status': 'success', 'message': 'Welcome to NIFTY Prediction API'})

if __name__ == '__main__':
    print("Starting Flask app...")
    print("API will be available at: http://localhost:5000")
    print("Health check: http://localhost:5000/api/health")
    print("Test endpoint: http://localhost:5000/api/test")
    app.run(host='0.0.0.0', port=5000, debug=True)
