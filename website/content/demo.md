Title: Demo
Date: 2019-04-06
Modified: 2019-04-07
Authors: Catarina Silva

##**Demo 03-04-2019**

### Demo - Platform

This demo shows how the physical sensors are connected to the virtual counterparts, and how the later ones can be used by external applications.
The physical sensor is the laptop itself.
A simple python script was used to read the CPU temperature and fan load (in rpm).
The sensor was connected to the eclipse hono through [MQTT](http://mqtt.org/), which in turn is connected to eclipse ditto through [AMPQ v1](http://www.amqp.org/). It was possible to see the data in the non-relational database used in the project ([Cassandra](http://cassandra.apache.org/)).
The laptop was used as a physical sensor because it was a simple sensor to show in the demonstration. However, all the sensors connected to the platform will behave in this manner.

These images show the example of the plot that you can see if run the demo:

When running the demo you can see variations:

![plot00]({filename}/images/plot00.png)

A few minutes later with a program running:

![plot01]({filename}/images/plot01.png)

###Setup the demo
The following steps are necessary to run the demo:

- Hono - Register tenant
- Hono - Register device
- Add hashed password of the device
- Ditto - Register demo
- Ditto - Add mapping function (convert JSON from Hono to Ditto JSON structure)

You can see support code for this task at code ua repository ([here](http://code.ua.pt/projects/pei-2018-2019-g12/repository/revisions/master/show/servers/demo01))

### Run the demo

`./start.sh`

###You can find the slides of the first demo [here](https://drive.google.com/open?id=114BphSNuX1EyIssy0W-XPOwNBrEFrCEy)

