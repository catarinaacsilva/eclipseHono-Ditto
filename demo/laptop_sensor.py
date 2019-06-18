# coding: utf-8


import os
import time
import json
import signal
import logging
import argparse
import paho.mqtt.client as mqtt


# configure logger output format
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',datefmt='%m-%d %H:%M:%S')


# used to stop the infinity loop
done = False


def exit(signalNumber, frame):  
    global done
    done = True
    return


def main(args):
    # get a logger to write
    logger = logging.getLogger('sensor') 
    
    # register handler for interruption 
    # it stops the infinite loop gracefully
    signal.signal(signal.SIGINT, exit)

    # MQTT client
    client = mqtt.Client('', protocol=mqtt.MQTTv311)
    client.username_pw_set(args.l+'@'+args.t, password=args.p)
    client.enable_logger()
    logger.info('Connect to %s', args.a)
    client.connect(args.a)
    client.loop_start()

    while not done:
        cpu_load = os.getloadavg()
        msg = json.dumps({'CPU_Load': cpu_load[0]})
        client.publish('e', msg, qos=1)
        logger.info('MSG %s', msg)
        time.sleep(args.r)

    client.loop_stop()
    client.disconnect()
    
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='laptop sensor')
    parser.add_argument('-a', type=str, help='ip address Hono', default='192.168.85.107')
    parser.add_argument('-t', type=str, help='hono tenant', default='demo')
    parser.add_argument('-l', type=str, help='login', default='laptop-auth')
    parser.add_argument('-p', type=str, help='password', default='password')
    parser.add_argument('-r', type=int, help='refresh rate', default='1')
    args = parser.parse_args()
    main(args)
