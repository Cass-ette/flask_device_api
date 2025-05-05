# 设备管理 API

## 🚀 快速开始
```bash
# 安装依赖
pip install -r requirements.txt

# 初始化数据库（自动创建）
python app.py

# 测试API（另开终端）
curl http://localhost:5000/devices
```

## 📚 API 文档
| 端点 | 方法 | 描述 |
|------|------|------|
| `/devices` | GET | 获取所有设备 |
| `/devices/<id>` | GET | 获取特定设备 |
| `/devices` | POST | 添加新设备 |
| `/devices/<id>` | PUT | 更新设备 |
| `/devices/<id>` | DELETE | 删除设备 |

## 🔧 请求示例
```json
// POST /devices
{
  "device_id": "device1",
  "name": "Living Room Light",
  "status": "on",
  "energy_usage": 15.5
}

// PUT /devices/device1
{
  "status": "off"
}
```

## 🗄️ 数据库结构
```sql
CREATE TABLE devices (
    device_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    status TEXT NOT NULL,
    energy_usage REAL NOT NULL
);
```