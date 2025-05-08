import os
import sqlite3
from flask import Flask, jsonify, request
from devices import SmartHomeHub, Light, Thermostat, Camera  # 新增导入

app = Flask(__name__)
app.config['DATABASE'] = '/app/instance/devices.db'

# 初始化数据库和设备
def init_db():
    with app.app_context():
        conn = sqlite3.connect(app.config['DATABASE'])
        conn.execute('''CREATE TABLE IF NOT EXISTS devices
                        (device_id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        type TEXT NOT NULL,    -- 新增类型字段
                        status TEXT NOT NULL,
                        energy_usage REAL NOT NULL);''')
        conn.commit()
        
        # 加载已有设备到内存
        hub = SmartHomeHub()
        cursor = conn.execute('SELECT * FROM devices')
        for row in cursor.fetchall():
            device_id, name, dev_type, status, energy = row
            # 根据类型创建对应设备对象
            if dev_type == 'Light':
                device = Light(device_id, name, energy_usage=energy)
            elif dev_type == 'Thermostat':
                device = Thermostat(device_id, name, energy_usage=energy)
            elif dev_type == 'Camera':
                device = Camera(device_id, name, energy_usage=energy)
            else:
                device = Device(device_id, name, energy_usage=energy)
            
            device.turn_on() if status == 'on' else device.turn_off()
            hub.controller.add_device(device)
        
        conn.close()

os.makedirs('/app/instance', exist_ok=True)
init_db()  # 初始化数据库

# 获取设备统一方法
def get_hub():
    return SmartHomeHub()

# 带设备状态同步的API
@app.route('/smart-hub/devices', methods=['GET'])
def get_smart_devices():
    hub = get_hub()
    devices = []
    for device in hub.controller.devices.values():
        # 构建详细设备信息
        device_data = {
            "id": device.get_id(),
            "name": device.get_name(),
            "status": device.get_status(),
            "energy_usage": device.get_energy_usage(),
            "type": device.__class__.__name__
        }
        # 添加设备特有属性
        if isinstance(device, Light):
            device_data["brightness"] = device.get_brightness()
        elif isinstance(device, Thermostat):
            device_data["temperature"] = device.get_temperature()
        elif isinstance(device, Camera):
            device_data["resolution"] = device.get_resolution()
        devices.append(device_data)
    
    return jsonify({
        "devices": devices,
        "total_energy": hub.total_energy_usage()
    })

@app.route('/devices', methods=['POST'])
def add_device():
    data = request.get_json()
    device_id = data.get('device_id')
    name = data.get('name')
    dev_type = data.get('type')  # 必须提供设备类型
    
    # 参数校验
    if not all([device_id, name, dev_type]):
        return jsonify({"error": "Missing required fields"}), 400
    
    # 创建对应设备对象
    device_map = {
        "Light": Light,
        "Thermostat": Thermostat,
        "Camera": Camera
    }
    if dev_type not in device_map:
        return jsonify({"error": "Invalid device type"}), 400
    
    device = device_map[dev_type](
        device_id=device_id,
        name=name,
        energy_usage=data.get('energy_usage', 0)
    )
    
    # 状态设置
    if data.get('status') == 'on':
        device.turn_on()
    
    # 数据库操作
    conn = sqlite3.connect(app.config['DATABASE'])
    try:
        conn.execute('INSERT INTO devices VALUES (?,?,?,?,?)', 
                    (device_id, name, dev_type, 
                     device.get_status(), device.get_energy_usage()))
        conn.commit()
        
        # 添加到内存控制器
        hub = get_hub()
        hub.controller.add_device(device)
        
        return jsonify({"message": "Device added"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Device ID exists"}), 409
    finally:
        conn.close()

@app.route('/devices/<device_id>/command', methods=['POST'])
def control_device(device_id):
    hub = get_hub()
    data = request.get_json()
    
    # 验证设备存在
    if device_id not in hub.controller.devices:
        return jsonify({"error": "Device not found"}), 404
    
    # 执行命令并同步状态
    command = data.get('command')
    if command in ['on', 'off']:
        # 更新内存状态
        hub.controller.execute_command(device_id, command)
        
        # 更新数据库状态
        conn = sqlite3.connect(app.config['DATABASE'])
        conn.execute('UPDATE devices SET status=? WHERE device_id=?', 
                    (command, device_id))
        conn.commit()
        conn.close()
        
        return jsonify({"message": f"Device {command} successful"})
    
    return jsonify({"error": "Invalid command"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
