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




The ESP32 receives measurements from the LM35 temperature sensor and the YL-38 rain sensor. It sends the temperature value to the server, as well as a value of 1 in case of rain and 0 when there is no rain.

The server receives the data, authenticates the user, and if the credentials are correct, it stores the data in a MySQL database. It checks the temperature value and sends a command to the client to activate cooling when the temperature exceeds 24°C and deactivate it when it drops below 22°C. If the rain value is 1, it sends an email to the user notifying them that it has started raining. To avoid repeated emails, the server checks the values from the last hour and only sends an email if the latest value is 1 and all previous values are 0.

The server displays the latest temperature value on a webpage, along with the average of the measurements from the last hour. User login is required to access the webpage.
