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
the connections were made on the back of the board according to the schematics down below:

- Red wire: power (3.3V)
- Black wire: Ground
- Blue wire: SCA and data
- Purple wire: SDA


![our circuit](https://user-images.githubusercontent.com/107586157/176541063-b7465c39-da76-41f2-b240-bf56e5ab83b7.jpg)
# Code & Thingspeak

