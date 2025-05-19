# IoT Weather Monitoring & Automation System

**End-to-End IoT Solution with Smart Environmental Control**  
*ESP32 Embedded System → Python/MySQL Backend → Automated Actions*

## System Overview

A robust IoT architecture that:
1. **Collects** environmental data via ESP32 + sensors
2. **Processes** data on a Python/Flask server with user authentication
3. **Stores** measurements in a MySQL database (time-series format)
4. **Triggers** smart actions based on configurable thresholds
5. **Visualizes** data through a secure web dashboard

## Technical Highlights

### Embedded System (ESP32)
- **Precision Sensing**:
  - LM35 Temperature Sensor (±0.5°C accuracy)
  - YL-38 Rain Detection (Digital trigger)
- **Optimized Communication**:
  - HTTP POST every 5 minutes (300k ms interval)
  - JSON payload compression
  - WiFi reconnection logic

### Backend (Python/Flask)
```python
@app.route('/addvalue', methods=['POST'])
def addvalue():
    # Data validation
    if cleartext['server_id'] == 'S03237a':
        # Database insertion
        mycursor.execute("INSERT INTO sensors24 VALUES (%s,%s,%s,%s)", 
                        (device, temp, rain_status, timestamp))
        # Smart Actions:
        if temp > 24: return 'Turn on A/C'
        elif temp < 22: return 'Turn off A/C'
        if rain_detected(): send_rain_alert()
```
