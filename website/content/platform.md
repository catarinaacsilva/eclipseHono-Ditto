Title: Platform-Documentation
Date: 2019-04-07
Modified: 2019-04-12
Category: Documentation
Tags: Hono, Ditto, Cassandra, mqtt, bridge, AMQP v1 
Authors: Catarina Silva


<center>***Technology innovations in hardware, networking and software are fueling the opportunity for new IoT solutions and use cases***</center>

<p>The Internet of Things (IoT) is transforming how individuals and organizations connect with customers, suppliers, partners, and other individuals.  
IoT is all about connecting sensors, actuators, and devices to a network and enabling the collection, exchange, and analysis of generated information. So, connectivity is at the heart of IoT solutions. Devices need to be connected to a back-end component where the data and functionality of the devices is leveraged to provide some higher level business value.</p> 

A typical IoT solution is characterized by many devices that may use some form of gateway to communicate through a network to an enterprise back-end server that is running an IoT platform that helps integrate the IoT information into the existing enterprise. The roles of the devices, gateways, and platform are well defined, and each of them provides specific features and functionality required by any robust IoT solution.

The IoT Platform represents the software infrastructure and services required to enable an IoT solution. It is expected to scale both horizontally, to support the large number of devices connected, as well as vertically to address the variety of IoT solutions.

<p>The core features of an IoT Platform include:</p>

- **Connectivity and Message Routing** – IoT platforms need to be able to interact with very large numbers of devices and gateways using different protocols and data formats, but then normalize it to allow for easy integration into the rest of the enterprise.

- **Device Management and Device Registry** – a central registry to identify the devices/gateways running in an IoT solution and the ability to provision new software updates and manage the devices.

- **Data Management and Storage** – a scalable data store that supports the volume and variety of IoT data.

- **Event Management, Analytics & UI** – scalable event processing capabilities, ability to consolidate and analyze data, and to create reports, graphs, and dashboards.

- **Application Enablement** – ability to create reports, graphs, dashboards, … and to use API for application integration.

##**Eclipse Hono**

<center>![hono]({filename}/images/hono.png)</center>

<p>Eclipse Hono consists of a set of micro services provided as Docker images.</p>

<p>The main purpose of Hono is to provide a uniform API for applications to interact with devices, regardless of the particular communication protocol the devices natively use. In order to do so, Hono uses a unique logical identifier to refer to each device individually.</p>

**Overview**
<p>Eclipse Hono is written entirely in Java. It also provides a uniform messaging infrastructure for IoT solutions. Eclipse Hono offers:</p>

- a horizontally scalable microservice architecture
- a design for container-based cloud environments (based on AMQP 1.0)
- load protection for all microservices using AMQP 1.0 flow control
- protocol adapters for different IoT protocols
- handling of different communication patterns
- a tenant-based security model, including authentication of device

<center>![title]({filename}/images/title.png)</center>

<p>Hono specifically supports scalable and secure ingestion of large volumes of sensor data by means of its Telemetry and Event APIs. Hono's Command and Control API allows for sending commands (request messages) to devices and receive a reply to such a command from a device in an asynchronous way.</p>
<center>![honoPlatform]({filename}/images/honoPlatform.png)</center>

Hono does not make any assumptions about the format of a device identifier (or device-id for short). Once registered, the device can be referred to by this identifier when using Hono’s APIs until the device is unregistered.

Hono supports the logical partitioning of devices into groups called tenants. Each tenant has a unique identifier, a string called the tenant-id, and can be used to provide a logical grouping of devices belonging. Each device can thus be uniquely identified by the tuple (tenant-id, device-id).

<p>It's necessary:</p>

- **Device Registration** – Hono components use the Device Registration API to access device registration information.
<center>![honoEsquema]({filename}/images/esquemahono2.png)</center>
<p>*FileBasedCredentialsService*, *FileBasedTenantService* and *FileBasedRegistrationService*: store all data in the local file system</p>
- **Device Authentication** – Devices connect to protocol adapters in order to publish telemetry data or events. In order to support the protocol adapters in the process of verifying credentials presented by a device, the Credentials API provides means to look up secrets on record for the device and use this information to verify the credentials. 

<p>The Credentials API supports registration of multiple sets of credentials for each device. A set of credentials consists of an auth-id and some sort of secret information. The particular type of secret determines the kind of information kept. Please refer to the Standard Credential Types defined in the Credentials API for details. Based on this approach, a device may be authenticated using different types of secrets, e.g. a hashed password or a pre-shared key, depending on the capabilities of the device and/or protocol adapter.</p>

###Connectivity and Protocol Support - Hono

**Top Level**
<center>![honoEsquema]({filename}/images/esquemahono1.png)</center>
<p>The MQTT and HTTP Adapters use the Device Registry to authenticate Devices connecting to the adapters and asserting their registration status. The adapters then forward the telemetry data and events received from the devices to the AMQP 1.0 Messaging Network for delivery to Business Applications. Business applications also use the messaging network to send commands to connected devices.</p>

**AMQP 1.0 Messaging Network**
<p>A few properties of the AMQP 1.0 messaging protocol make it an ideal candidate for this purpose. First, this is one of very few messaging protocols that is truly symmetrical. It does not require a broker as an intermediary in the message exchange process. It supports both “store and forward” and direct messaging communication patterns. The symmetrical nature of AMQP 1.0 allows Hono to use different communication semantics and different messaging components to handle various flows of messages. Another important feature of AMQP 1.0 is its flow control mechanism, which is implemented directly in the protocol. This means that consumers will, at every point, declare their capacity, or how many messages should be delivered to them. </p>

Hono comes with a default implementation of the messaging network relying on artifacts provided by other open source projects. The default implementation currently consists of a single [Apache Qpid Dispatch Router](https://qpid.apache.org/) instance connected to a single [Apache Artemis](https://activemq.apache.org/components/artemis/) broker instance.

 Apache QPid Dispatch Router provides direct communication between producing and consuming endpoints. Apache Artemis Broker provides a scalable AMQP 1.0 message broker.

<center>![honoEsquema]({filename}/images/esquemahono3.png)</center>


###Features at a glance

- Secure message dispatching
- Support for different message exchange patterns
- Provides interfaces to support implementation of protocol adaptors
- Sending telemetry data
- Receiving device control messages (from applications/solutions)
- Registering authorized consumers of telemetry data received from connected devices

---

##**Grafana**
<p>[Grafana](https://grafana.com/) is an open-source platform for data visualization, monitoring and analysis. </p>

<center>![grafana]({filename}/images/grafana.png)</center>

- A Grafana instance providing a dashboard visualizing the collected metrics data.

---

##**Eclipse Ditto**

<center>![ditto]({filename}/images/ditto.png)</center>

<p>Eclipse Ditto is a technology in the IoT implementing a software pattern called “Digital Twins”. A Digital Twin is a virtual, cloud based, representation of his real world counterpart.</p>

The technology mirrors potentially millions and billions of digital twins residing in the digital world with physical Things. This simplifies developing IoT solutions for software developers as they do not need to know how or where exactly the physical “Things” are connected.

**Concept: Thing in the context of Eclipse Ditto**
<p>Things are very generic entities and are mostly used as a “handle” for multiple features belonging to this Thing.</p>

Thing can be:

- Physical Device
- Virtual Device
- Transactional entity
- Master data entity
- Anything else - if it can be modeled and managed appropriately by the supported concepts/capabilities.  

With Eclipse Ditto a Thing can just be used as any other web service via its digital twin. For Eclipse Ditto the Digital Twin is a concept for abstracting a real world device with all capabilities and aspects including its digital representation.

**What are digital twins in the context of Eclipse Ditto?**
<p>Digital twins are mainly a mechanism for simplifying IoT solution development. A digital twin mirrors physical devices in the cloud. On the one hand, it allows access to specific aspects of a device, enabling you, for example, to evaluate device data. On the other hand, digital twins offer the opportunity to provide additional services around the device, such as enhancing the virtual representation of a device with weather data, or by adding information about its spare parts. The digital twins concept often also includes the simulation of devices. You can create a digital twin of a device before it’s even manufactured or deployed. You can then simulate the device in use before it is deployed in the real world and use the APIs before the device begins sending data. </p>

<p>A Digital Twin:</p>

- mirrors physical devices
- acts as a “single source of truth” for a physical asset
- provides various aspects and services around devices
- keeps real and digital worlds in sync
- can be applied in both industrial and consumer-centric IoT scenarios


<p>Eclipse Ditto provides a framework that enables you to work with, and manage, the state of digital twins. It builds the bridge between real-world IoT devices and their digital twins.</p>

<p>A Digital Twin framework:</p>

- provides capabilities (APIs) to interact with Digital Twins
- ensures that access to twins can only be done by authorized parties
- allows to not only interact with single twins but also with populations of many of them
- integrates into other back-end infrastructure (like messaging systems, brokers)

<p>Eclipse Ditto 0.8.0 focuses on providing advanced capabilities in building and working with the digital twins pattern.
Building and exposing digital twins is possible via different APIs: HTTP/REST, WebSockets, AMQP 1.0, AMQP 0.9.1 and MQTT 3.1.1 are supported.</p>

On all APIs, Ditto ensures that only authorized subjects may interact (read/write) with the digital twins with the use of fine grained policies.

Ditto can establish a connection to Eclipse Hono and optionally transform received messages to “Ditto Protocol” (protocol Ditto defined for twin interaction). 
Powerful devices may alternatively directly send their data to Ditto’s HTTP/WebSocket endpoints in order to reflect changes made to them.

For integrating with Eclipse Hono this version of Eclipse Ditto makes it possible to subscribe to telemetry/events from devices connected via Hono and to also send command&control messages to devices connected to Hono and correlate replies from Hono accordingly.

###Authentication and authorization
On all APIs Ditto protects functionality and data by using:

- Authentication to make sure the requester is the one she claims to be,
- Authorization to make sure the requester is allowed to see, use or change the information he wants to access. 

###Characteristics of Messages

Eclipse Ditto is not a message broker and does not want to offer features a message broker does.

Ditto:

- Offers no message retention. If a device isn’t connected when a Message should be routed, it will never receive the Message.
- Makes no statement about Message QoS. Messages are routed at most once.
- Does deliver messages only in “fan out” style, if the same credentials are connected twice, both connections will receive Messages if the credential is authorized to read a Message.

**Messages can be sent via:**

- the WebSocket API as Ditto Protocol messages
- the HTTP API either as “fire and forget” messages or, when expecting a response, in a blocking way at the Messages HTTP API endpoint

If you want to send a Message to or from a Thing, you need WRITE permissions on that Thing. Every WebSocket that is able to receive Messages for the Thing (READ permission), will receive your message.

**Receiving Messages**
<p>To be able to receive Messages for a Thing, you need to have READ access on that Thing. When a Message is sent to or from a Thing, every connected WebSocket with the correct access rights will receive the Message. If there is more than one response, only the first one will be routed back to the initial issuer of a Message.</p>
Currently, you can only respond to Messages using the Ditto Protocol WebSocket binding



---
##**Apache Cassandra**

<center>![cassandra]({filename}/images/cassandra.png)</center>

<p>Apache Cassandra is a free and open-source, distributed, wide column store, NoSQL database management system designed to handle large amounts of data across many commodity servers, providing high availability with no single point of failure. </p>

A NoSQL database is a type of data processing engine that can be deployed exclusively for working with data that can be stored in tabular format and hence does not meet the requirements of relational databases. Some of the salient features of NoSQL databases are that they can handle extremely large amounts of data, have a simple API, can be replicated easily, they are practically schema-free and are more or less consistent.

The Apache Cassandra database is the right choice when you need scalability and high availability without compromising performance. Linear scalability and proven fault-tolerance on commodity hardware or cloud infrastructure make it the perfect platform for mission-critical data. Cassandra's support for replicating across multiple datacenters is best-in-class, providing lower latency for your users and the peace of mind of knowing that you can survive regional outages.


<center>![honoPlatform]({filename}/images/eclipseFoundation.png) ![honoPlatform]({filename}/images/eclipseIncubation.png) ![honoPlatform]({filename}/images/apacheFoundation.png)</center>