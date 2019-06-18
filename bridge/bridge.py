# coding: utf-8


__author__ = 'Catarina Silva'
__version__ = '0.3'
__email__ = 'c.alexandracorreia@ua.pt'
__status__ = 'Development'


import json
import logging
import argparse
from datetime import datetime
from proton.reactor import Container
from proton.handlers import MessagingHandler
from detimotic.storage import InfluxDB, Cassandra
from detimotic.ditto import Ditto
from detimotic.utils import Cache, json_to_features, is_json
from detimotic.device_mapper import DeviceMapper


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('BRIDGE')


URI='amqp://consumer%40HONO:verysecret@192.168.85.107:15672'


# Check if a int port number is valid
# Valid is bigger than base port number
def check_port(port, base=1024):
    value = int(port)
    if value <= base:
        raise argparse.ArgumentTypeError('%s is an invalid positive int value' % value)
    return value


# Hono handler
class HonoHandler(MessagingHandler):
    def __init__(self, addr, port, user, pwd, influx, cassandra, ditto):
        super(HonoHandler, self).__init__()
        self.addr = addr
        self.port = port
        self.user = user
        self.pwd = pwd
        self.influx = influx
        self.cassandra = cassandra
        #self.dm = dm
        self.ditto = ditto
        self.cache = Cache()

    def on_start(self, event):
        conn = event.container.connect(str(self.addr) + ":" + str(self.port), user=self.user, password=self.pwd)
        event.container.create_receiver(conn, 'event/*')
        event.container.create_receiver(conn, 'telemetry/*')
        event.container.create_receiver(conn, 'control/*')

    def on_message(self, event):
        resource = event.message.annotations['resource']
        timestamp = datetime.fromtimestamp(event.message.creation_time)
        [queue, tenant_id, device_id] = resource.split('/')
        value = event.message.body.decode('UTF-8')
        logger.debug('Message %s %s %s %s %s', queue, tenant_id, device_id, timestamp, value)
        self.cassandra.store(queue, tenant_id, device_id, timestamp, value)

        if is_json(value):
            self.influx.store(queue, tenant_id, device_id, timestamp, value)
            #self.dm.map(tenant_id, device_id, value)
            key = (tenant_id, device_id)
            logger.debug('Map the following device %s:%s = %s', tenant_id, device_id, value)
            if key not in self.cache:
                logger.debug('Device %s:%s not in cache...', tenant_id, device_id)
                if not self.ditto.thing_exists(tenant_id, device_id):
                    logger.debug('Device %s:%s  does not exists in Ditto...', tenant_id, device_id)
                    rv = self.ditto.thing_create(tenant_id, device_id,
                    {'tenant':tenant_id, 'device':device_id, 'mapper':__version__}, json_to_features(value))
                    logger.debug('Create device = %s', rv)
                    rv = self.ditto.devops_piggyback_create_hono_mapping(tenant_id, device_id, URI, value)
                    logger.debug('Map device = %s', rv)
                    self.cache.update(key, True)
                else:
                    logger.debug('Device %s:%s already exists in Ditto', tenant_id, device_id)
            else:
                logger.debug('Device %s:%s in cache...', tenant_id, device_id)


def main(args):
    try:
        ditto = Ditto()
        #dm = DeviceMapper()
        influx = InfluxDB(args.addr_influxdb, args.port_influxdb, args.influxdb_user, args.influxdb_pwd, args.influxdb_database)
        cassandra = Cassandra(args.addr_cassandra, args.cassandra_user, args.cassandra_pwd, args.cassandra_keyspace)
        Container(HonoHandler(args.addr_hono, args.port_hono, args.hono_user, args.hono_pwd, influx, cassandra, ditto)).run()
    except KeyboardInterrupt:
        influx.close()
        cassandra.close()
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DETImotic Bridge (Hono <-> Storage)')
    #parser.add_argument('--addr_hono', type=str, help='ip address Hono', default='detimotic-1-pei2019.5g.cn.atnog.av.it.pt')
    parser.add_argument('--addr_hono', type=str, help='ip address Hono', default='192.168.85.107')
    parser.add_argument('--port_hono', type=check_port, help='ip port Hono', default=15672)
    parser.add_argument('--hono_user', help='hono user', default="consumer@HONO")
    parser.add_argument('--hono_pwd', help='hono password', default="verysecret")

    #parser.add_argument('--addr_cassandra', type=str, help='ip address Cassandra', default='detimotic-2-pei2019.5g.cn.atnog.av.it.pt')
    parser.add_argument('--addr_cassandra', type=str, help='ip address Cassandra', default='192.168.85.101')
    parser.add_argument('--cassandra_user', help='cassandra user', default='detimotic')
    parser.add_argument('--cassandra_pwd', help='cassandra password', default='detimotic')
    parser.add_argument('--cassandra_keyspace', help='cassandra keyspace', default='detimotic')
    
    #parser.add_argument('--addr_influxdb', type=str, help='ip address influxdb', default='detimotic-2-pei2019.5g.cn.atnog.av.it.pt')
    parser.add_argument('--addr_influxdb', type=str, help='ip address influxdb', default='192.168.85.101')
    parser.add_argument('--port_influxdb', type=check_port, help='ip port influxdb', default='8086')
    parser.add_argument('--influxdb_user', help='influxdb user', default='detimotic')
    parser.add_argument('--influxdb_pwd', help='influxdb password', default='detimotic')
    parser.add_argument('--influxdb_database', help = 'influx database', default = 'detimotic')
    args = parser.parse_args()
    main(args)
