#include <Arduino.h>
#include <HardwareSerial.h>
#include "TinyGPS++.h"

// Initialize TinyGPSPlus object
TinyGPSPlus gps;
HardwareSerial SerialGPS(1);

void setup()
{
    // Start the built-in Serial port for debugging
    Serial.begin(115200);

    // Start the GPS hardware serial port
    SerialGPS.begin(9600, SERIAL_8N1, 16, 17); // Example with UART1 on GPIO16 (RX) and GPIO17 (TX)

    Serial.println("GPS Module Test");
}

void loop()
{
    while (SerialGPS.available() > 0) 
    {
        gps.encode(SerialGPS.read());
    }

    if (gps.location.isUpdated()) 
    {
        Serial.print("Latitude: ");
        Serial.println(gps.location.lat(), 6);
        Serial.print("Longitude: ");
        Serial.println(gps.location.lng(), 6);
    }

    delay(1000);
}