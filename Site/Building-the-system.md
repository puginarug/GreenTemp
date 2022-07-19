# Components
In order to build one measuring station we used the following parts:
1. 1x <a href=http://esp32.net/>ESP32.</a><br>
    
2. 2x <a href=https://www.adafruit.com/product/2857>SHT31</a> I2C temprature and humidity sensors.<br>
    
3. 1x <a href=https://www.adafruit.com/product/2717>TCA9548A</a> I2C Multiplexer.<br>
    
4. 4x <a href=https://components101.com/sensors/ds18b20-temperature-sensor>DS18B20</a> Thermometers (more can be connected)<br>
    
5. 1x 4.7kΩ Resistor
6. 1x <a href=https://www.electricaltechnology.org/2019/11/12v-to-5v-converter-circuit.html>buck converter</a> 12V to 5V (didactable if chosen to connect via USB)<br>
    

in order to assmble it on top of the prototype board we had to use some Male to Female mounts that were souldred to the board itself. a 3-wire connector and two 4 wire connectors. The circuit itself was assembled with thin coated wires that were wire turned on top of the souldered pins. the SHT-31 sensors were all connected via 4 core wire and mounts that we crimped on to the wires. Similarly done we took four 4 core wires that were crimped in one side and braided them in order to connect the DS18B20
<p align="center">
<img src="https://user-images.githubusercontent.com/107586157/179503265-cf8b6dca-74e1-472b-b501-014e89592f5e.jpg"
 width="250">
<img src="https://user-images.githubusercontent.com/107586157/179503285-519fa5cc-1895-463d-bb79-a580dbd000da.jpg"
 width="250">
</p>



the finnished board looked like this:
<p align="center">
<img src="https://user-images.githubusercontent.com/107586157/176545093-fced8147-ff82-42ee-ba7c-0c1321bde8c0.jpg" width="500">
</p>



# Instructions
We made 3 copies of the circuit that is shown below, in order to take temperature samples from all over the greenhouse.
For each circuit:
- We've soldered the required components to a stripboard, whereas components that are more expensive or reusable (ESP32, multiplexers, etc.) were not soldered directly, but had attachments that were soldered to the stripboard. 

<p align="center">
<img src="https://user-images.githubusercontent.com/107586157/179499913-a73bff3c-98ab-454f-9c52-4b709d5014f8.jpg"
 width="500">
</p>

- The cables of the circuit it self were wire turned on top of the pins sticking from the bottom of the board.
The end product eventually looked like this:
<p align="center">
<img src="https://user-images.githubusercontent.com/107586157/179501659-e907ddfa-2379-4350-8548-bf6f3d85b60d.jpg"
 width="500">
</p>

- We connected each sensor to a cable, in order to give us more flexibility with the project placement and for exceeding the measuring range of the project. the cables were made as mensioned above with a crimper.
- Each board was encapsulated in a humidity-proof plastic box in order to keep the electric components dry and safe.
- The project is powered by a 12V power source, which is converted to a 5V with the help of a buck-converter.
- Each box is placed in the desired locations, according to the researcher's interest.


<p align="center">
    <img src="https://media1.giphy.com/media/xUNd9Z3IC4IwJ1uLjG/giphy.gif?cid=ecf05e47fbe75gfwukjvw7pw0nf0wnh708c2cdkuaogn1j3m&rid=giphy.gif&ct=g" width="240" height="180" frameBorder="0">
</p>

# Our Circuit Diagram
the connections were made on the back of the board according to the schematics down below:

- Red wire: power (3.3V)
- Black wire: Ground
- Blue wire: SCA and data
- Purple wire: SDA
![our circuit](https://user-images.githubusercontent.com/107586157/176541063-b7465c39-da76-41f2-b240-bf56e5ab83b7.jpg)





