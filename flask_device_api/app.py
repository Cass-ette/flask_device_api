import sqlite3
import os
from flask import Flask, jsonify, request
from devices import SmartHomeHub

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(os.getcwd(), 'instance', 'devices.db')
os.makedirs(os.path.dirname(app.config['DATABASE']), exist_ok=True)

# 初始化智能家居中心
hub = SmartHomeHub()

def get_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.execute('''CREATE TABLE IF NOT EXISTS devices
                    (device_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    energy_usage REAL NOT NULL)''')
    return conn

# 设备数据库API
@app.route('/devices', methods=['GET'])
def get_all_devices():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM devices')
    devices = [dict(zip(['device_id','name','status','energy_usage'], row)) 
               for row in cursor.fetchall()]
    conn.close()
    return jsonify(devices)

@app.route('/devices/<device_id>', methods=['GET'])
def get_device(device_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM devices WHERE device_id=?', (device_id,))
    device = cursor.fetchone()
    conn.close()
    return jsonify(dict(zip(['device_id','name','status','energy_usage'], device))) if device else ('Not found', 404)

@app.route('/devices', methods=['POST'])
def add_device():
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO devices VALUES (?,?,?,?)',
                      (data['device_id'], data['name'], data.get('status','off'), data.get('energy_usage',0.0)))
        conn.commit()
        return jsonify({'message': 'Device added'})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Device exists'}), 409
    finally:
        conn.close()

# 智能家居控制API
@app.route('/smart-hub/devices', methods=['GET'])
def get_smart_devices():
    return jsonify([{
        'id': d.get_id(),
        'name': d.get_name(),
        'type': d.__class__.__name__,
        'status': d.get_status()
    } for d in hub.controller.devices.values()])

@app.route('/smart-hub/<device_id>/<command>', methods=['POST'])
def control_device(device_id, command):
    device = hub.controller.get_device(device_id)
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    if command == 'on':
        device.turn_on()
    elif command == 'off':
        device.turn_off()
    else:
        return jsonify({'error': 'Invalid command'}), 400
    return jsonify({'message': f'Device {device_id} turned {command}'})

if __name__ == '__main__':
    # 初始化测试设备
    hub.controller.add_device(Light('L1', 'Living Room Light'))
    hub.controller.add_device(Thermostat('T1', 'Living Room Thermostat'))
    app.run(host='0.0.0.0', port=5000)
