#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <TinyGPS++.h>
#include <ArduinoJson.h>

#include "personal_credentials.h"

TinyGPSPlus gps;
HardwareSerial SerialGPS(1);
String gpsServer = "http://192.168.1.250:5000/gps";

void setup()
{
    Serial.begin(115200);

    // SSID and Password are stored in the personal credentials header file.
    Serial.print("Connecting to: "); Serial.println(WIFI_SSID);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.println("Connecting...");
        delay(1000);
    }
    Serial.print("Connected to Wifi with local IP: "); Serial.println(WiFi.localIP());

    // Set up GPS UART communication
    SerialGPS.begin(9600, SERIAL_8N1, 16, 17); // GPIO16 is RX and GPIO17 is TX

    
}

void loop()
{
    while (SerialGPS.available() > 0)
    {
        gps.encode(SerialGPS.read());
    }
    // See if we have a satellite found
    int satellites = gps.satellites.value();
    Serial.println("Satellites found: " + String(satellites));


    if (gps.location.isUpdated())
    {
        float latitude = gps.location.lat();
        float longitude = gps.location.lng();


        Serial.println("Latitude: " + String(latitude));
        Serial.println("Longitude: " + String(longitude));

        uint8_t hour;
        uint8_t minute;
        uint8_t second;

        if (gps.time.isUpdated())
        {
            hour = gps.time.hour();
            minute = gps.time.minute();
            second = gps.time.second();
        }

        // Only make HTTP requests if we are still connected to the internet
        if (WiFi.status() == WL_CONNECTED)
        {
            // Create a JSON object
            DynamicJsonDocument jsonDoc(200);
            jsonDoc["latitude"] = latitude;
            jsonDoc["longitude"] = longitude;
            jsonDoc["satellites"] = satellites;
            
            jsonDoc["hour"] = hour;
            jsonDoc["minute"] = minute;
            jsonDoc["second"] = second;

            // Serialization into a string
            String payload;
            serializeJson(jsonDoc, payload);

            // Make an HTTP request
            HTTPClient http;
            Serial.println("Server Address: " + gpsServer);

            http.begin(gpsServer);
            http.addHeader("Content-Type", "application/json");
            int httpResponseCode = http.POST(payload);

            if (httpResponseCode > 0)
            {
                Serial.println("HTTP Response Code: " + String(httpResponseCode));
                String response = http.getString();
                Serial.println("Response: " + response);
            } else 
            {
                Serial.println("HTTP Request Failed: " + String(http.errorToString(httpResponseCode)));
            }

            http.end();
        }

    }
    
    Serial.println();
    delay(2000);    // Post data every 2 seconds
}