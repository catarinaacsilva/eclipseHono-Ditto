Title: Client
Date: 2019-03-06
Modified: 2019-03-06
Category: Client
Tags: Client
Authors:

Nowadays, IoT is a buzzword for those who work with technology. The Internet of Things refers to the concept of extending Internet connectivity beyond conventional computing platforms such as personal computers and mobile devices, into any range of everyday and conventional devices. Embedded with electronics, Internet connectivity and hardware (e.g sensors), these devices can communicate and interact with others over the Internet, and they can be remotely controlled and monitored. The definition of IoT has evolved due to convergence of a wide variety of technologies, machine learning and artificial intelligence. Traditional fields of embedded systems, wireless sensor networks (e.g Wifi, LoRa), control systems and automation contribute to enabling more and more complex IoT solutions. 
DETI holds a large number of sensors and intends to install them in its building to improve its habitability through the efficient use of the departments infrastructure and equipment.



##**Proposed solution**

Install and configure a system of sensors managed by a central platform, provide the use strategy (API) and documentation for future iterations and develop a set of use cases for the sensors data (“a proof of concept”).

##**Technical requirements**

- Sensors must prioritize connecting to the iot server via gateways, in order to filter telemetry dimension. (scalability) 
- Most sensors should use LoRa as the communication protocol, since its decreases the number of sensor gateways(due to increased range vs WiFi) and installation costs.

##**Schedule of features**

#### version 1
Install and make a barebones system functional on DETI’s MakerLab.

**Sensor system**:

- MultiConnect conduit gateway
- 1x sensor with LoRa communication
- Server with eclipse hono

#### version 2
Expand to WiFi.
	
**Sensor system**:

- MultiConnect conduit gateway
- 1x sensor with LoRa communication
- server with eclipse hono
- Raspberry PI gateway
- 1x sensor with WiFi communication

#### version 3
Full set of sensors.

**Sensor system**:

- MultiConnect conduit gateway
- Raspberry PI gateway
- server with eclipse hono
- camera
	- Current
	- Co2
	- Temperature
	- Humidity

##**Risks and issues**

- Budget restrictions
- Number and variety of sensors available to use could be limited
- The place where we will install the sensors may be constrained by the location and the number of power plugs
- Some extra hardware needs to be ordered, so it’s crucial to identify what components are necessary in a very premature phase of - The project to have them in, ready to use.



