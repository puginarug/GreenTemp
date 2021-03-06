# Code and Cloud Usage
In this section we will dicuss the code and cloud setup for our project. the esp32 is programmed with C++ and the data collected was uploaded to <a href="https://thingspeak.com/">ThingSpeak</a>. Each one of our boxes has a channel where u can find its measurments:

- <a href=https://thingspeak.com/channels/1777871> Box 1</a>
- <a href=https://thingspeak.com/channels/1766721> Box 2</a>
- <a href=https://thingspeak.com/channels/1777982> Box 3</a>

All of the code used in this project is found in the 'Code' folder.

## Preparation


In order to proceed with the code make sure the following libraries are installed:
- OneWire
- Adafruit_Unified_Sensor
- Adafruit_SHT31_Library
- DallasTemperature
- ThingSpeak

If you dont know how to add a library please consult this <a href=https://create.arduino.cc/projecthub/akshayjoseph666/adding-library-in-arduino-ide-7deb01>guide</a>.

after installing all the relevant libraries we shall proceed.
first of all is finding the DS18B20 addresses. in order to read this component the address is needed, each one has a unique address so it lets us read pretty much as many as we want (as long as we have its address).
In order to find the address we first need to assemble the next circuit:
<p align="center">
<img src="https://user-images.githubusercontent.com/107586157/177033550-8902eeaa-9344-484f-84fa-824816cc395d.jpg" width="350">
</p>

Now we are going to find the address of each one of the DS18B20 sensors. 
In order to do that, flash to your ESP32  'find_DS18B20.ino' that can be found in the code file or coppied from here:
```C++
#include <OneWire.h>

// Based on the OneWire library example

OneWire ds(33);  //data wire connected to GPIO 33

void setup(void) {
  Serial.begin(115200);
}

void loop(void) {
  byte i;
  byte addr[8];
  
  if (!ds.search(addr)) {
    Serial.println(" No more addresses.");
    Serial.println();
    ds.reset_search();
    delay(250);
    return;
  }
  Serial.print(" ROM =");
  for (i = 0; i < 8; i++) {
    Serial.write(' ');
    Serial.print(addr[i], HEX);
  }
}
```


After getting the addresses we proceeded to connect the sensors via the cables we made. We used the  'symphonyOfSensors.ino' to integrate all of our components, it can be found in the code file or coppied from here.
``` C++
//including all libararies 
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_SHT31.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <WiFi.h>
#include "ThingSpeak.h"

unsigned long myChannelNumber = 1777982;// ThingsSpeak Channek number
const char * myWriteAPIKey = "XTQKABJ4IVJX2YDR";//ThingsSpeak Channel write API
const char* ssid = "agrotech-lab-1"; // your wifi SSID name
const char* password = "1Afuna2Gezer" ;// wifi pasword
const char* server = "api.thingspeak.com";
WiFiClient client;

#define ONE_WIRE_BUS 19// Data wire is connected to GPIO19

OneWire oneWire(ONE_WIRE_BUS);
// Pass our oneWire reference to Dallas Temperature sensor 
DallasTemperature sensors(&oneWire);
DeviceAddress sensor1 = { 0x28, 0xFF, 0x64, 0x2, 0xEF, 0xFE, 0xBA, 0xD0 };// Defining our DS18B20 addresses
DeviceAddress sensor2 = { 0x28, 0xFF, 0x64, 0x2, 0xEF, 0xFC, 0xEB, 0xC4 };
DeviceAddress sensor3= { 0x28, 0xFF, 0x64, 0x2, 0xEF, 0x9D, 0x7A, 0x15 };
DeviceAddress sensor4= { 0x28, 0xFF, 0x64, 0x2, 0xEF, 0x37, 0xD9, 0x51 };

Adafruit_SHT31 sht31 = Adafruit_SHT31(); //Defining the SHT31 as objects to refer
Adafruit_SHT31 sht1; // I2C SHT31
Adafruit_SHT31 sht2; // I2C SHT31

float sht1_t,sht2_t,h1,h2,ds1,ds2,ds3,ds4;//Defining global temperature and humidity variables


// Defining a function that selects the required bus of the multiplexer
void TCA9548A(uint8_t bus)// Select I2C BUS
{
  Wire.beginTransmission(0x70);  // TCA9548A address
  Wire.write(1 << bus);          // send byte to select bus
  Wire.endTransmission();
}


void insert_temps()// Defining a function that collects all the temperatures from the different 
{                  
  TCA9548A (6); // In order to read the relevant sht we first need to switch to its bus 
  sht1_t=sht1.readTemperature()+0.22;
  h1=sht1.readHumidity();
  TCA9548A (7);
  sht2_t=sht2.readTemperature()+0.56;
  h2=sht2.readHumidity();
  ds1=sensors.getTempC(sensor1)-1.27;\\reading the temperatue and adding the relevant margin so the sensors will be calibrated
  ds2=sensors.getTempC(sensor2)+0.03;
  ds3=sensors.getTempC(sensor3)+0.33;
  ds4=sensors.getTempC(sensor4)+0.14;
}


void Wifi()// Defining a function that connects to the wifi
{
  WiFi.disconnect();
  delay(10);
  WiFi.begin(ssid, password);
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  ThingSpeak.begin(client);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("NodeMcu connected to wifi...");
  Serial.println(ssid);
  Serial.println();
}


void Upload_TS() //Defining a function that upload our data to ThingSpeak
{
  ThingSpeak.setField(1,sht1_t);
  ThingSpeak.setField(2,sht2_t);
  ThingSpeak.setField(3,ds1);
  ThingSpeak.setField(4,ds2);
  ThingSpeak.setField(5,ds3);
  ThingSpeak.setField(6,ds4);
  ThingSpeak.setField(7,h1);
  ThingSpeak.setField(8,h2);
  ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);
}


void setup() 
{
  Serial.begin(115200);// Starting the connection with the esp32
  Wifi(); // connecting to the wifi
  sensors.begin(); // Start I2C communication with the Multiplexer
  Wire.begin();

  // Initial set up for sensor on bus number 6
  TCA9548A(6);
  if (!sht1.begin(0x44)) {
    Serial.println("Could not find a valid SHT31 sensor on bus , check wiring!");
    while (1);
  }
  Serial.println();
  
  // Initial set up for sensor on bus number 7
 TCA9548A(7);
  if (!sht2.begin(0x44)) {
    Serial.println("Could not find a valid SHT31 sensor on bus , check wiring!");
    while (1);
  }
  Serial.println();
}

void loop() { 
  sensors.requestTemperatures();// Send the command to get temperatures from DS18B20
  insert_temps(); // Reading the temperatures via the function we wrote
  Upload_TS(); // Uploading our data to ThingSpeak
  delay(5000);
}
```
Go ahead and boot it to your ESP32.

Optional but useful is calibrating the sensors by calculating the mean and adding the margins to each sensor.
