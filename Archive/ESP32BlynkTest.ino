#define BLYNK_TEMPLATE_ID "TMPL6UFMf4x3F"
#define BLYNK_TEMPLATE_NAME "ESP32Test"
#define BLYNK_AUTH_TOKEN "6PafxZoNXxmj3ScK7qyjMBngBUaG0oA9"
// Comment this out to disable prints and save space
#define BLYNK_PRINT Serial

#include <WiFi.h>
#include <WiFiClient.h>
#include <BlynkSimpleEsp32.h>

char auth[] = BLYNK_AUTH_TOKEN;

int led1 = 22;
int led2 = 23;
int pot = 34;

BLYNK_WRITE(V0)
{
    int pinValue = param.asInt();
    digitalWrite(led1, pinValue);
}

BLYNK_WRITE(V1)
{
    int pinValue = param.asInt();
    digitalWrite(led2, pinValue);
}

void setup()
{
    pinMode(led1, OUTPUT);
    pinMode(led2, OUTPUT);
    pinMode(pot, INPUT);
    // Debug console
    Serial.begin(115200);

    Blynk.begin(auth, "Wokwi-GUEST", "");
}

void loop()
{
    Blynk.run();
    int potvalue = analogRead(pot);
    // Serial.print("pot = ");
    // Serial.println(potvalue);
    Blynk.virtualWrite(V2, potvalue);
    String terminalStr = "pot = ";
    terminalStr.concat(potvalue);
    // String terminalStr = "pot = " + potvalue;
    Serial.println(terminalStr);
    Blynk.virtualWrite(V3, terminalStr);
}