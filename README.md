# IoT Weather Monitoring & Automation System

A Flask-based web application that collects temperature and rain data from an ESP32 sensor, stores it in a MySQL database, and displays it on a dashboard with real-time alerts.

## Features
- **ESP32 Sensor**: Measures temperature (LM35) and rain status.
- **Flask Backend**: REST API for data ingestion and web dashboard.
- **MySQL Database**: Stores historical sensor data.
- **Email Alerts**: Sends warnings when rain is detected.
- **AC Control**: Automatically suggests AC on/off based on temperature thresholds.
- **User Authentication**: Secure login system.

## Hardware Requirements
- ESP32 microcontroller
- LM35 temperature sensor
- Rain sensor (YL-83)
- Relay module (for AC control)

## Software Requirements
- Python 3.x
- Flask
- MySQL
- MySQL Connector/Python
- Arduino IDE (for ESP32 firmware)-