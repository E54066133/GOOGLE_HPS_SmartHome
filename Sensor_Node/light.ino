#include <Wire.h>
#include <BH1750.h>
#include <SoftwareSerial.h>

SoftwareSerial BTSerial(2, 3); // RX | TX
BH1750 lightMeter;

void setup() 
{
  Serial.begin(9600);
  Wire.begin();

  lightMeter.begin();
  BTSerial.begin(9600);
}

void loop() 
{
  int lux = lightMeter.readLightLevel();
  delay(1000);

  int z = 0;
  if (lux > 10000) {
    byte data[5];
    data[0] = lux / 10000;
    lux=lux%10000;
    data[1] = lux / 1000;
    lux=lux%1000;
    data[2] = lux / 100;
    lux=lux%100;
    data[3] = lux / 10;
    data[4] = lux % 10;
    
    BTSerial.write(data, sizeof(data));
  }
  
  else if (lux > 1000) {
    byte data[4];
    data[0] = lux / 1000;
    lux=lux%1000;
    data[1] = lux / 100;
    lux=lux%100;
    data[2] = lux / 10;
    data[3] = lux % 10;
    
    BTSerial.write(data, sizeof(data));

  }
  else if (lux > 100){
    byte data[3];
    data[0] = lux / 100;
    lux=lux%100;
    data[1] = lux / 10;
    data[2] = lux % 10;
    BTSerial.write(data, sizeof(data));
  }
  else {
    byte data[2];

    data[0] = lux / 10; 
    data[1] = lux % 10;
    BTSerial.write(data, sizeof(data));
  }
  delay(300000); 
}
