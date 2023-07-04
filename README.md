
# Light, humidity and temperature sensor
Tom Enqvist\
te222qz

This project will demonstarte how to measure light, temperature and humidity using dht11 sensors and photo resistors. To make it somewhat more reliable for use with action triggers, the readings are averaged and over time and by using 2 of each sensor. Outlier readings are also disregarded when calculating the average.

Temperature, humidity, light values and darkness percentage are sent to io.adafruit.com for vizualisation and logging.

It will take aproximately 3 hours to complete given no problems are encountered during software and hardware installation.

## Objective

The main reason I've choosen this project to learn how to use the dht11 sensor and photo reistor. During the making of the project I found out the sensors (especially the photo reistor) sometimes reported readings that would differ far too much from what was expected. These spikes in the reading could make the data "noisy" and unwantedly trigger actions. So, a secondary reason I've choosen this project is to try to make the readings more reliable for this usecase.

The purpose of the project is to report and log light, humidity and temperature values, and based on these values trigger actions via webhooks.

This project will give insight on the environment it is placed in. In my case, I've placed it on my balcony to gain insight on sunset and sundown timings and corresponding temperature and humidity level.

## Material

| Material | Description |  |
| --- | -------- | - |
| DHT11 | Temperature and Humidity Sensor |[link](https://www.electrokit.com/produkt/digital-temperatur-och-fuktsensor-dht11/)|
| Photo Resistor | Light dependant resistor for reading light level | [link](https://www.electrokit.com/produkt/ljussensor/)
|Breadboard 840 connections | | [link](https://www.electrokit.com/produkt/kopplingsdack-840-anslutningar/)
|Jumper cables (Male to male)|| [link](https://www.electrokit.com/produkt/labbsladd-20-pin-15cm-hane-hane/)
|USB cable|| [link](https://www.electrokit.com/produkt/usb-kabel-a-hane-micro-b-5p-hane-1-8m/)
|Optional) Jumper cables (Male to female)|| [link](https://www.electrokit.com/produkt/labbsladd-40-pin-30cm-hona-hane/)
|(Optional) Breadboard 270 connections|| [link](https://www.electrokit.com/produkt/kopplingsdack-270-anslutningar/)
||| [link]()

Explain all material that is needed. All sensors, where you bought them and their specifications. Please also provide pictures of what you have bought and what you are using.

- List of material
- What the different things (sensors, wires, controllers) do - short specifications
- Where you bought them and how much they cost

## Computer setup

For the purpose of this project I have used Visual Studio as my IDE

How is the device programmed. Which IDE are you using. Describe all steps from flashing the firmware, installing plugins in your favorite editor. How flashing is done on MicroPython. The aim is that a beginner should be able to understand.

- Chosen IDE
- How the code is uploaded
- Steps that you needed to do for your computer. Installation of Node.js, extra drivers, etc.

## Putting everything together

How is all the electronics connected? Describe all the wiring, good if you can show a circuit diagram. Be specific on how to connect everything, and what to think of in terms of resistors, current and voltage. Is this only for a development setup or could it be used in production?

- Circuit diagram (can be hand drawn)


## Platform

Describe your choice of platform. If you have tried different platforms it can be good to provide a comparison.

Is your platform based on a local installation or a cloud? Do you plan to use a paid subscription or a free? Describe the different alternatives on going forward if you want to scale your idea.

- Describe platform in terms of functionality


## The code

### Connecting to a network

The boot.py file makes sure the pico is connected to a network using Wifi. SSID and passwords are stored in secrets.py

https://github.com/tomenqvist/project_v2/blob/651fe7cd284308049c1e42ea8408e6b2f0e07ca0/src/boot.py#L1-L51

### Sensors
In the sensors.py file we need to first import necessary libraries and create and populate our queues for storing sensor values

https://github.com/tomenqvist/project_v2/blob/651fe7cd284308049c1e42ea8408e6b2f0e07ca0/src/sensors.py#L1-L27

We also need to implement functions for dealing with queues (the deque library did not work for me)

https://github.com/tomenqvist/project_v2/blob/651fe7cd284308049c1e42ea8408e6b2f0e07ca0/src/sensors.py#L124-L129

This is the function for reading and calculating mean light values:

https://github.com/tomenqvist/project_v2/blob/651fe7cd284308049c1e42ea8408e6b2f0e07ca0/src/sensors.py#L54-L120

The light values of each sensor are stored in the queue, and then a sorted copy of the are created from which the mean value are calculated from position 2 to 7, meaning outliers (position 0, 1, 7 and 8) are disregarded. Then the mean value of those two values are calculated and returned. 

The darkness percentage are also calculated by using the min and max light value from the last 7 days.

*The function for reading values from the DHT11 sensor works in basically the same way*

### Main

First we need to import libraries and set user, password, key and paths to adafruit topics and at waht rate we want to send the data. 

**Remenber to include the mqtt.py file in your project since MQTT is used to send data to adafruit**

https://github.com/tomenqvist/project_v2/blob/651fe7cd284308049c1e42ea8408e6b2f0e07ca0/src/main.py#L1-L25

Then we create a function for sending the data, and finally we run an infinite loop that calls the sensor and send_data functions:

https://github.com/tomenqvist/project_v2/blob/651fe7cd284308049c1e42ea8408e6b2f0e07ca0/src/main.py#L27-L74

## Transmitting the data / connectivity

How is the data transmitted to the internet or local server? Describe the package format. All the different steps that are needed in getting the data to your end-point. Explain both the code and choice of wireless protocols.

- How often is the data sent?
- Which wireless protocols did you use (WiFi, LoRa, etc …)?
- Which transport protocols were used (MQTT, webhook, etc …)

## Presenting the data

Describe the presentation part. How is the dashboard built? How long is the data preserved in the database?

- Provide visual examples on how the dashboard looks. Pictures needed.
- How often is data saved in the database.

## Finalizing the design

Show the final results of your project. Give your final thoughts on how you think the project went. What could have been done in an other way, or even better? Pictures are nice!

- Show final results of the project
- Pictures
