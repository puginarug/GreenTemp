# GreenTemp
Temporal and spatial temperature measurement in a greenhouse - Agrotech course final project.
Our main goals:
1. Having fun 🥳
2. Examining the change of temperatures inside the greenhouse as a function of:
    - The height of the sample point.
    - The distance of the sample point from the greenhouse's cooling pad system.

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

![A GIF](/Images/giphy.gif)
<p>
    <img src="/Images/giphy.gif" width="480" height="360" frameBorder="0">
</p>

# Our Circuit Diagram
the connections were made on the back of the board according to the schematics down below:

- Red wire: power (3.3V)
- Black wire: Ground
- Blue wire: SCA and data
- Purple wire: SDA
![our circuit](https://user-images.githubusercontent.com/107586157/176541063-b7465c39-da76-41f2-b240-bf56e5ab83b7.jpg)
# Code & Thingspeak
### Preperation ###
All of the code used in this project is found in the 'Code' folder.

In order to proceed with the code make sure the following libraries are installed:
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

Now we are going to find the address of each one of the DS18B20 sensors. 
In order to do that, flash the code inside of 'find_DS18B20.ino' to your ESP32.

After getting the addresses we proceeded and built the circuit mentioned above. We used the code found in 'symphonyOfSensors.ino' to integrate all of our components.
Go ahead and boot it to your ESP32.




# Data Analysis
In order to get a 3d plot containing the current temperatures from all the sensor, run the code from the attached file: 'Agtech_final_project_3D_Temp_plotting'.

Example for a 3d plot generated by the code:
![16 07 22 13 00PM](https://user-images.githubusercontent.com/101471376/179350166-53a21ea5-4fd9-4407-a724-bfb912f72c4f.png)


