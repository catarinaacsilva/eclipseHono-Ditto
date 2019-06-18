Title: Detimotic
Date: 2019-03-10
Modified: 2019-04-7
Category: Information
Tags: IoT, M2M, Context Information
Authors: Catarina Silva
Save_As: index.html

 
The DETImotic project is related to IoT, M2M and domotics. The project's focus is to capture sensory data from several sensors spread through the department and expose an API that can be used by several users to develop smarter applications. Furthermore, the platform is a testbed for IoT and M2M scenarios, that can be used by all students.

- The data gathered by the sensors is an asset, that can be exploited in order to improve resource allocation, improve health conditions (information on the levels of carbon dioxide), among others.

- Relevant information can be acquired by analyzing the data captured by sensors, making it possible to improve and optimize the department resources.  

- The system benefits from a vast collection of sensors (not only physical sensors but documentation and code samples).

- The platform was deployed in IT Aveiro servers, while the physical sensors will be spread amongst the  DETI (Department of Electronics, Telecommunications and Informatics) of University of Aveiro. 
- Although the product will be deployed inside DETI (hence the name), the sensors can be used to any building.

- This website contains enough documentation to re.deploy the system in another building.

**The fundamental idea is to create a platform of excellence for IoT data acquisition and IoT scenario testing.**

The platform will provide the following assets:

1. Requires a registration (portal) integrated with the [IDP](http://api.web.ua.pt/pt/services/universidade_de_aveiro/oauth) of the university
2. You can see the documentation about the platform and how to access  it in this website
3. Samples of the sensors code are available on our repository
4. Custom dashboard

**What is the platform? What is this integrate?**

The platform is composed of 4 components:

- [Eclipse Hono](https://www.eclipse.org/hono/getting-started/)
- [Eclipse Ditto](https://www.eclipse.org/ditto/)
- [Apache Cassandra](http://cassandra.apache.org/)
- Portal (for registry and user iteration with the system)

All these components are interconnected through bridges that respect the protocols that each of them supports. All of these bridges were developed in python.
The portal is used to mediate the access and functionality between the end users and the components of the platform.

In short, you can interact with the system through the Portal. The Portal will implement the following functionality:

1. Register devices and users in the platform (physical and virtual counterparts)
2. List registered sensors
3. Remove registered sensors
4. Access persistent storage
4. Access a custom  dashboard

Next image shows the simplified platform's architecture.

![platform]({filename}/images/demo01.png)

For detailed information regarding the platform, please check [Architecture](http://xcoa.av.it.pt/~pei2018-2019_g012/pages/architecture.html).



*This project was developed at Deti in Aveiro University and Instituto de Telecomunicações*
![deti]({filename}/images/deti.png)
![ua]({filename}/images/ua.png)
![it]({filename}/images/it.png)



