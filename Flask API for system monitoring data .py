from flask import Flask, jsonify, request, send_from_directory
import psutil
import os
import time
import platform
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Get system info
def get_system_info():
    try:
        if platform.system() == 'Windows':
            # Windows doesn't provide direct boot_time, so calculate it from uptime
            uptime = psutil.boot_time()  # For debugging, log the uptime
            logging.debug(f"Uptime on Windows: {uptime}")
            boot_time_epoch = time.time() - uptime
            boot_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(boot_time_epoch))
        else:
            uptime = psutil.boot_time()  # For debugging, log the uptime
            logging.debug(f"Uptime on Unix-like OS: {uptime}")
            boot_time_epoch = psutil.boot_time()
            boot_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(boot_time_epoch))
        
        # Check if the boot_time value is valid
        if not boot_time:
            boot_time = 'Invalid Date'  # If boot time retrieval fails
            logging.error(f"Boot time invalid: {boot_time}")
    except Exception as e:
        boot_time = 'Invalid Date'
        logging.error(f"Error fetching boot time: {e}")

    memory = psutil.virtual_memory()
    network = psutil.net_io_counters()
    users = psutil.users()

    return {
        "boot_time": boot_time,
        "memory": {
            "total": memory.total,
            "used": memory.used,
            "available": memory.available,
            "percent": memory.percent,
        },
        "network": {
            "bytes_sent": network.bytes_sent,
            "bytes_recv": network.bytes_recv,
        },
        "users": [{"name": user.name, "host": user.host} for user in users],
    }

# Get CPU usage
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

# Get disk usage
def get_disk_usage():
    disk = psutil.disk_usage('/')
    return {
        "total": disk.total,
        "used": disk.used,
        "free": disk.free,
        "percent": disk.percent,
    }

# Get running processes
def get_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        try:
            processes.append({
                "pid": proc.info['pid'],
                "name": proc.info['name'],
                "username": proc.info['username'],
                "cpu_percent": proc.info['cpu_percent'],
                "memory_percent": proc.info['memory_percent']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processes

# Run a new task
def run_task(command):
    try:
        os.system(command)
        return {"message": f"Command '{command}' executed successfully!"}
    except Exception as e:
        return {"message": f"Error executing command: {e}"}

# Kill a process by PID
def kill_process(pid):
    try:
        process = psutil.Process(pid)
        process.kill()
        return {"success": True, "message": f"Process {pid} terminated successfully."}
    except psutil.NoSuchProcess:
        return {"success": False, "message": f"Process {pid} does not exist."}
    except Exception as e:
        return {"success": False, "message": f"Error terminating process {pid}: {e}"}

# API Routes

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/system_status', methods=['GET'])
def system_status():
    system_info = get_system_info()
    return jsonify({
        "cpu_usage": get_cpu_usage(),
        "memory": system_info["memory"],
        "disk": get_disk_usage(),
        "boot_time": system_info["boot_time"],
        "network": system_info["network"],
        "users": system_info["users"]
    })

@app.route('/api/processes', methods=['GET'])
def processes():
    return jsonify(get_processes())

@app.route('/api/kill_process', methods=['POST'])
def kill():
    data = request.get_json()
    pid = data.get('pid')
    if pid is not None:
        kill_response = kill_process(pid)
        updated_processes = get_processes()
        return jsonify({
            "success": kill_response["success"],
            "message": kill_response["message"],
            "processes": updated_processes
        })
    return jsonify({"success": False, "message": "No PID provided"}), 400

@app.route('/api/run_task', methods=['POST'])
def run_new_task():
    data = request.get_json()
    command = data.get('command')
    if command:
        return jsonify(run_task(command))
    return jsonify({"message": "No command provided"}), 400

@app.route('/api/run_command', methods=['POST'])
def run_command():
    data = request.get_json()
    command = data.get('command')
    if command:
        try:
            output = os.popen(command).read()
            return jsonify({"output": output})
        except Exception as e:
            return jsonify({"output": f"Error: {e}"})
    return jsonify({"output": "No command provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
