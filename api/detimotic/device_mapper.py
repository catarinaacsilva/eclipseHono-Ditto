# coding: utf-8


__author__ = 'Catarina Silva'
__version__ = '0.2'
__email__ = 'c.alexandracorreia@ua.pt'
__status__ = 'Development'


import json
import logging
import requests
from .utils import is_json


logger = logging.getLogger('MAPPER API')


class DeviceMapper:

    def __init__(self, addr='192.168.85.101', port=80):
        self.addr = addr
        self.port = port
    
    def map(self, tenant, device, data):
        if is_json(data):
            j = {'tenant': tenant, 'device': device, 'json': json.loads(data)}
            url = 'http://{}:{}/map'.format(self.addr, self.port)
            response = requests.post(url, json=j)
            logger.info('Map: %s', j)
            if int(response.status_code//100) == 2:
                return True
        return False
