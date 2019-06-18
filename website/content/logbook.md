Title: Logbook
Date: 2019-03-06
Modified: 2019-04-07
Category: Updates
Tags: Personas
Authors: Catarina Silva

##**Week 1**
**Comment 1:** In addition to the sensors that will be programmed/configured and integrated into the IoT platform, several other functionalities could be developed making the department even smarter (as stated previously). As of now, no limitation has yet arisen since the sensors to be used are available and ready to use. In relation to complementary material such as servers have also been made available. We intend to respect the established use cases but it is important to mention that the development of this project assumes that other sensing devices could be added in the future. Thus, one of our goals will be to provide good documentation of everything done in such a way that the current work is simple to understand and replicate, furthermore future additions will be easy to implement and maintain.

- Architecture development
- Formatting srv1 (DETI server room 120)

##**Week 2**

- Creating RAID 5 (ZFS)
- Proxmox installation
- Network configuration

**Comment 1:** Some problems in access to the server because VPN of UA improve some restrictions and it's necessary to solve. We talked with sTIC (responsible for UA network) but until the moment they have a solution for the problem. As of now, alternatives are being analyzed.


##**Week 3**

- Deployed two servers: one for storage ([Cassandra](http://cassandra.apache.org/)) and the other for the bridge ([Hono](https://www.eclipse.org/hono/))
- Formatted and installed Ubuntu 18.04, as the base OS for the servers
- Configured the communication on both servers (ssh, key pair, authentication) 
- Deployed Cassandra on one of the servers
- Creation and configuration of a static website (Pelican)
- Write a manual

##**Week 4**

- Deployed Hono on the remaining server
- Configured initial schema on the database 
- Implemented the first version of a bridge that connect Hono with Cassandra
- Correction of the site
- Preparation of the documentation
- Start to study of the Ditto
- Preparation of installation of the Ditto

##**Week 5**

- Installation of the ditto
- Machine configuration
- Update site
- Gathering requirements for registration service

**comment 1:**Integration between ditto and hono requires a non-trivial registration service (requires mapping functions between sensor formats)

##**Week 6**

- Creating and registering a sensor (CPU temperature and fan speed) for demo
- Inserted manual mapping (without registration portal) between physical sensor and virtual counterpart
- Preparing first demo (code in the repository)
- Web site refactor (50%)


##**Week 7**

- Restructured DB to support new queries
- Change site to support documentation (more information, new theme, new menu scheme)
- Study of idp (oauth 1 vs oauth 2)
- Architecture design to support University of Aveiro (UA) idp

##**Week 8**

- Devised a new schema for the DB
- Migration the old schema to the new one 
- Review the kapua framework and the semantic associated with hono queues:telemetry, control and event
- Review and add new content to the website
- Revision of authentication methods
