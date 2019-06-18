Title: Architecture
Date: 2019-03-06
Modified: 2019-04-07
Category: Updates
Tags: Hardware, Raspberry Pi, Arduino, ESP8266, ESP32, Database
Authors: Catarina Silva


The sensor system will be deployed in a star-of-stars topology composed of sensors, gateways and the necessary servers. The sensor's microcontrollers connect to the gateways using the appropriate protocol and these connect to the IoT server thourgh MQTT over IP. Raspberry pies will be used as gateways for the sensors that communicate through WiFi. For every other sensor using the Lora protocol(allowing for wider coverage), the gateway is a MultiConnect Conduit which we’ll configure using its AEP interface. The platform servers are deployed in three different VMs, running Ubuntu. Each server runs one of the following components: [Eclipse Hono](https://www.eclipse.org/hono/), [Eclipse Ditto](https://www.eclipse.org/ditto/) and [Apache Cassandra](http://cassandra.apache.org/).

##**System Architecture**

![platform]({filename}/images/platform.png)

##**Sensor Architecture**