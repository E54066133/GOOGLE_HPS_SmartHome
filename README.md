# GOOGLE_HPS_SmartHome
2022 Taiwan Google Hardware Sprint Team 9

## Sensor Node
Through the HC-08 bluetooth module, Arduino sends sensor data like temperature, relative moisture, and light intensity to Raspberry Pi. Then, Raspberry Pi saves sensor data as txt file, and controls the wireless Tapo P110 switches to open the home appliances according to the data collected.           
             
![](https://github.com/E54066133/GOOGLE_HPS_SmartHome/blob/main/Sensor_Node/Image/1.jpeg)


## LineBot
Through RichMenu & Postman, users can just click the menu botten to interact with our linebot sever. 
The functions available to users :
1. See present condition outside the door
2. Check present temperature
3. Check present moisture
4. Check present light intensity
5. Set the smart_home settings

(In addtional, some functions are implemented by regular expression)
