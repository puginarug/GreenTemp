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