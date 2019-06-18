Title: Requirements
Date: 2019-03-06
Modified: 2019-04-08
Category: Updates
Tags: Vision, Scenarios
Authors: Catarina Silva

##**Platform (Developers)**
To deploy your own version of the platform you will need to install Eclipse Hono, Eclipse Ditto and Apache Cassandra. Apache Cassandra was chosen for this project because it's scale vertically maintaining fairly high performance.
Due to the communication model of each component, it is advisable to have three different servers (machines) for this implementation.

In a general way, it's necessary:

- Three servers/machines With [caracteristicas]
- Install Eclipse Hono
- Install Eclipse Ditto
- Install and configure database (Cassandra)

For the system it's necessary to interconnect:

- Eclipse Hono and Eclipse Ditto
- Eclipse Hono and Cassandra
- Eclipse Hono to Portal
- Eclipse Ditto to Dashboard
- Sensors to Eclipse Hono

In the platform documentation section, more details are given regarding the implementation.

The source code can be cloned (using Git) or downloaded from the [DETImotic Code ua repository](https://code.ua.pt/projects/pei-2018-2019-g12/repository).
In this repository, you can find every folders and readme (for folder) with all the information that you need to replicate the system.



