# coding: utf-8

__author__ = 'Catarina Silva'
__version__ = '0.1'
__email__ = 'c.alexandracorreia@ua.pt'
__status__ = 'Development'

import logging
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from influxdb import InfluxDBClient
from .utils import is_json, json_to_points


logger = logging.getLogger('STORAGE API')


class Cassandra:

    def __init__(self, host='localhost', user='', pwd='', keyspace='detimotic'):
        # Basic authentication
        auth_provider = PlainTextAuthProvider(username=user, password=pwd)
        self.cluster = Cluster([str(host)], compression='lz4', auth_provider=auth_provider)
        self.session = self.cluster.connect(keyspace)
        
        # Prepared Statements
        # Store statements
        self.insert_queue_tenant = self.session.prepare('INSERT INTO queue_tenant (queue, tenant) VALUES (?, ?) IF NOT EXISTS')
        self.insert_tenant_device = self.session.prepare('INSERT INTO tenant_device (tenant, device) VALUES (?, ?) IF NOT EXISTS')
        self.insert_values = self.session.prepare('INSERT INTO values (queue, tenant, device, timestamp, value) VALUES (?, ?, ?, ?, ?) IF NOT EXISTS')

    def store(self, queue, tenant, device, timestamp, data):
        self.session.execute(self.insert_queue_tenant, [queue, tenant])
        self.session.execute(self.insert_tenant_device, [tenant, device])
        self.session.execute(self.insert_values, [queue, tenant, device, timestamp, data])
        logger.debug('Store into Apache Cassandra: %s %s %s %s %s', queue, tenant, device, timestamp.isoformat(), data)
    
    def close(self):
        logger.debug('Close connection Apache Cassandra')
        self.cluster.shutdown()


class InfluxDB:

    def __init__(self, host='localhost', port='8086', user='detimotic', pwd='detimotic', database='detimotic'):
        self.client = InfluxDBClient(host=host, port=port, username=user, password=pwd, database=database)
    
    def store(self, queue, tenant, device, timestamp, data):
        logger.debug('Store into InfluxDB: %s %s %s %s %s', queue, tenant, device, timestamp.isoformat(), data)
        
        if is_json(data):
            points = json_to_points(queue, tenant, device, timestamp, data)
            logger.debug('%s', points)
            try:
                logger.debug(points)
                self.client.write_points(points, time_precision='ms')
            except Exception as e:
                logger.exception(e)
        else:
            logger.warning('Skip data; not json...')


    def close(self):
        logger.debug('Close connection InfluxDB')
        self.client.close()
