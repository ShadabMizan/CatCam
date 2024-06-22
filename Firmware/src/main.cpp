#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include "personal_credentials.h"

void setup()
{
    Serial.begin(115200);

    Serial.print("Connecting to: "); Serial.println(WIFI_SSID);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.println("Connecting...");
        delay(1000);
    }
    Serial.println("Connected.");
}

void loop()
{

}