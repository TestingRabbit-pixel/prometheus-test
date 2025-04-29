from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/test-endpoint', methods=['GET'])
def test_endpoint():
    worker_id = os.environ.get('WORKER_ID', 'unknown')
    return jsonify({
        "status": "success",
        "worker_id": worker_id,
        "message": "Test endpoint response",
        "data": {
            "test": True
        }
    })

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    message = data.get('message', '')
    worker_id = os.environ.get('WORKER_ID', 'unknown')
    return jsonify({
        "status": "success",
        "worker_id": worker_id,
        "message": "Message processed successfully",
        "data": {
            "processed_message": f"Processed: {message}",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 