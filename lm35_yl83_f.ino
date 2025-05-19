#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <string.h>

#define vRef 3.30
#define ADC_Resolution 4095
#define LM35_Per_Degree_Volt 0.01
#define Zero_Deg_ADC_Value 700.00
#define POWER_PIN 32  // ESP32's pin GPIO32 that provides the power to the rain sensor
#define DO_PIN 12     // ESP32's pin GPIO12 connected to DO pin of the rain sensor
const int relay = 26;
const int lm35_pin = A0;
float temp, ADC_Per_Degree_Val, temp_adc_val;

const char* ssid = "your ssid";
const char* password = "your password";
char payload[50];

unsigned long lastTime = 0;
// Set timer to 5 minutes (300000)
unsigned long timerDelay = 300000;


void setup() {
  Serial.begin(115200); 

  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

  digitalWrite(relay, HIGH);
  pinMode(relay, OUTPUT);
  pinMode(POWER_PIN, OUTPUT);  // configure the power pin as an OUTPUT
  pinMode(DO_PIN, INPUT);
  ADC_Per_Degree_Val = (ADC_Resolution/vRef)*LM35_Per_Degree_Volt;
}  


void loop() {
  
  if ((millis() - lastTime) > timerDelay) {
    
    if(WiFi.status()== WL_CONNECTED){

      for (int i = 0; i < 10; i++) {
        temp_adc_val += analogRead(lm35_pin);  // Read ADC value 
        delay(10);
      }
      temp_adc_val = temp_adc_val/10.0;
      temp_adc_val = temp_adc_val - Zero_Deg_ADC_Value;
      temp = (temp_adc_val/ADC_Per_Degree_Val);
      
      digitalWrite(POWER_PIN, HIGH);  // turn the rain sensor's power  ON
      delay(10);                      // wait 10 milliseconds
      int rain_state = digitalRead(DO_PIN);
      digitalWrite(POWER_PIN, LOW);  // turn the rain sensor's power OFF
   
    
      HTTPClient http;
      http.begin("http://192.168.31.252:4000/addvalue");      
      http.addHeader("Content-Type", "text/plain");
      
      StaticJsonDocument<200> doc;
      // Add values in the document

      doc["device_id"] = "A0131";
      doc["server_id"] = "S03237a";
      doc["temperature"] = temp;
      if (rain_state == HIGH)
        doc["rain_status"] = 0;
      else
        doc["rain_status"] = 1;
        

      String sendPostBody;
      serializeJson(doc, sendPostBody);
      Serial.println(sendPostBody);
      if (rain_state == HIGH)
        Serial.println("The rain is NOT detected");
      else
        Serial.println("The rain is detected");

      //Send HTTP POST request
      int httpResponseCode = http.POST(sendPostBody);


      if (httpResponseCode>0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        String payload = http.getString();
        Serial.println(payload);
        if (payload.indexOf("Turn on the A/C.") != -1) {
        Serial.println("The A/C has been turned on.");
        digitalWrite(relay, LOW); // turn on
      }else if (payload.indexOf("Turn off the A/C.") != -1) {
        Serial.println("The A/C has been turned off.");
        digitalWrite(relay, HIGH); // turn off
      }
      
      }
      else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
      }
      http.end();
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
}
