import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/smart-hub/devices', methods=['GET'])
def get_smart_devices():
    hub = SmartHomeHub()
    return jsonify({
        'devices': [str(device) for device in hub.controller.devices.values()],
        'total_energy': hub.total_energy_usage()
    })
    
def create_connection():
    conn = sqlite3.connect('devices.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS devices
                    (device_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    energy_usage REAL NOT NULL);''')
    return conn


@app.route('/devices', methods=['GET'])
def get_devices():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM devices')
    devices = cursor.fetchall()
    conn.close()
    result = [{'device_id': device[0], 'name': device[1],'status': device[2], 'energy_usage': device[3]} for device in devices]
    return jsonify(result)


@app.route('/devices/<device_id>', methods=['GET'])
def get_device(device_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM devices WHERE device_id =?', (device_id,))
    device = cursor.fetchone()
    conn.close()
    if device:
        result = {'device_id': device[0], 'name': device[1],'status': device[2], 'energy_usage': device[3]}
        return jsonify(result)
    return jsonify({'message': 'Device not found'}), 404


@app.route('/devices', methods=['POST'])
def add_device():
    data = request.get_json()
    device_id = data.get('device_id')
    name = data.get('name')
    status = data.get('status', 'off')
    energy_usage = data.get('energy_usage', 0.0)

    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO devices (device_id, name, status, energy_usage) VALUES (?,?,?,?)',
                       (device_id, name, status, energy_usage))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Device added successfully'})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'message': 'Device ID already exists'}), 409


@app.route('/devices/<device_id>', methods=['PUT'])
def update_device(device_id):
    data = request.get_json()
    name = data.get('name')
    status = data.get('status')
    energy_usage = data.get('energy_usage')

    conn = create_connection()
    cursor = conn.cursor()
    updates = []
    values = []
    if name:
        updates.append('name =?')
        values.append(name)
    if status:
        updates.append('status =?')
        values.append(status)
    if energy_usage:
        updates.append('energy_usage =?')
        values.append(energy_usage)
    values.append(device_id)

    if updates:
        update_query = 'UPDATE devices SET'+ ', '.join(updates) +'WHERE device_id =?'
        try:
            cursor.execute(update_query, tuple(values))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Device updated successfully'})
        except sqlite3.Error as e:
            conn.close()
            return jsonify({'message': f'Error updating device: {str(e)}'}), 500
    return jsonify({'message': 'No valid data to update'}), 400


@app.route('/devices/<device_id>', methods=['DELETE'])
def delete_device(device_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM devices WHERE device_id =?', (device_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Device deleted successfully'})
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'message': f'Error deleting device: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
