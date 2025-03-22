from flask import Flask, jsonify
import psutil

app = Flask(__name__)

@app.route('/api/system_status', methods=['GET'])
def get_system_status():
    status = {
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent
    }
    return jsonify(status)

if __name__ == '__main__':
    app.run(debug=True)
