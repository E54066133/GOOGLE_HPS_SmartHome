#include <Wire.h>
#include "DFRobot_SHT20.h"
#include <SoftwareSerial.h>

DFRobot_SHT20 sht20;
SoftwareSerial BTSerial(2, 3); // RX | TX

void setup()
{
  Serial.begin(9600);
  BTSerial.begin(9600);
  Serial.println("SHT20!");
  sht20.initSHT20();                         // Init SHT20 Sensor
  delay(100);
  sht20.checkSHT20();                        // Check SHT20 Sensor
}

void loop()
{
  int humd = sht20.readHumidity();         // Read Humidity
  int temp = sht20.readTemperature();      // Read Temperature
  Serial.print(humd);
  Serial.print(", ");
  Serial.println(temp);
  byte data[4];
  data[0] = humd/10;
  data[1] = humd%10;
  data[2] = temp/10;
  data[3] = temp%10;
  BTSerial.write(data, sizeof(data));
  delay(300000);
}
