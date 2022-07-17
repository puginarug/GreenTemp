# GreenTemp
Temporal and spatial temperature measurement in a greenhouse - Agrotech course final project.

# Building the circuit
In order to build one measuring station we used the following parts:
1. 1x ESP32.<br>
    http://esp32.net/
2. 2x SHT31 I2C temprature and humidity sensors.<br>
    https://www.adafruit.com/product/2857
3. 1x TCA9548A I2C Multiplexer.<br>
    https://www.adafruit.com/product/2717
4. 4x DS18B20 Thermometers (more can be connected)<br>
    https://components101.com/sensors/ds18b20-temperature-sensor
5. 1x 4.7kΩ Resistor
6. 1x buck converter 12V to 5V (didactable if chosen to connect via USB)<br>
    https://www.electricaltechnology.org/2019/11/12v-to-5v-converter-circuit.html

in order to assmble it on top of the prototype board we had to use some Male to Female mounts that were souldred to the board itself. a 3-wire connector and two 4 wire connectors. The circuit itself was assembled with thin coated wires that wire wire turned on top of the souldered pins and the sensors were all connected via 4 core wire and mounts that we crimped on to the wires.

the finnished board looked like this:
<p align="center">
<img src="https://user-images.githubusercontent.com/107586157/176545093-fced8147-ff82-42ee-ba7c-0c1321bde8c0.jpg" width="500">
</p>



# Instructions
We made 3 copies of the project that is shown below, in order to take temperature samples from all over the greenhouse.
For each project:
- We've soldered the required components to a stripboard, whereas components that are more expensive or reusable (ESP32, multiplexers, etc.) were not soldered directly, but had attachments that were soldered to the stripboard.
- We connected each sensor to a cable, in order to give us more flexibility with the project placement and for exceeding the measuring range of the project.
- Each board was encapsulated in a humidity-proof plastic box in order to keep the electric components dry and safe.
- The project is powered by a 12V power source, which is converted to a 5V with the help of a buck-converter.
- Each box is placed in the desired locations, according to the researcher's interest.
 
In this project, we were interested in taking samples and analyzing temperature points in the greenhouse, while examining the change of temperatures as a function of:
  1. The height of the sample point.
  2. The distance of the sample point from the greenhouse's cooling pad system.

# Our Circuit Diagram
the connections were made on the back of the board according to the schematics down below:

- Red wire: power (3.3V)
- Black wire: Ground
- Blue wire: SCA and data
- Purple wire: SDA
![our circuit](https://user-images.githubusercontent.com/107586157/176541063-b7465c39-da76-41f2-b240-bf56e5ab83b7.jpg)
# Code & Thingspeak
### Preperation ###
in order to proceed with the code make sure the following libraries are installed:
- OneWire
- Adafruit_Unified_Sensor
- Adafruit_SHT31_Library
- DallasTemperature
- ThingSpeak

after installing all the relevant libraries we shall proceed.
first of all is finding the DS18B20 addresses. in order to read this component the address is needed, each one has a unique address so it lets us read pretty much as many as we want as long as we have its address.
In order to find the address we first need to assemble the next circuit:
<p align="center">
<img src="https://user-images.githubusercontent.com/107586157/177033550-8902eeaa-9344-484f-84fa-824816cc395d.jpg" width="500">
</p>

upload the next code to the ESP32 in order to see the DS18B20 code:

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
  Serial.print(" ROM =");   //Printing the serial numbers of the sensors
  for (i = 0; i < 8; i++) {
    Serial.write(' ');
    Serial.print(addr[i], HEX);
  }
}
```
After getting our addresses we proceeded and built the circuit mentioned above. we used the next code to integrate all of our components:










```C++
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
  ds1=sensors.getTempC(sensor1)-1.27;
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
# Data Analysis
In order to get a 3d plot containing the current temperatures from all the sensor, run the code from the attached file: 'Agtech_final_project_3D_Temp_plotting'.

Example for a 3d plot generated by the code:
![16 07 22 13 00PM](https://user-images.githubusercontent.com/101471376/179350166-53a21ea5-4fd9-4407-a724-bfb912f72c4f.png)


