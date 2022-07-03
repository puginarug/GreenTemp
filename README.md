# GreenTemp
Temporal and spatial temperature measurement in a greenhouse - Agrotech course final project.
# Components

# Building the circuit
In order to build one measuring station we used the following parts:
1. 1x ESP32.
2. 2x SHT31 I2C temprature and humidity sensors.
3. 1x TCA9548A I2C Multiplexer.
4. 4x DS18B20 Thermometers (more can be connected)
5. 1x 4.7kΩ Resistor
6. 1x buck converter 12V to 5V (didactable if chosen to connect via USB)

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


