# coding: utf-8

__author__ = 'Catarina Silva'
__version__ = '0.2'
__email__ = 'c.alexandracorreia@ua.pt'
__status__ = 'Development'

import logging
import requests


#logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',datefmt='%m-%d %H:%M:%S')
logger = logging.getLogger('HONO API')


class Hono:
    def __init__(self, addr='192.168.85.107'):
        self.addr = addr

    def tenant_create(self, tenant):
        url = 'http://{}:28080/tenant/'.format(self.addr)
        response = requests.post(url, json={'tenant-id':tenant})

        print(response.status_code)
        if int(response.status_code//100) == 2:
            return True
        else:
            logger.error('%s: %s', response.status_code, response.text)
        return False

    def tenant_delete(self, tenant):
        url = 'http://{}:28080/tenant/{}'.format(self.addr, tenant)
        response = requests.delete(url)

        if int(response.status_code//100) == 2:
            return True
        else:
            logger.error('%s: %s', response.status_code, response.text)
        return False
    
    def device_create(self, tenant, device):
        url = 'http://{}:28080/registration/{}'.format(self.addr, tenant)
        response = requests.post(url, json={'device-id':device})

        if int(response.status_code//100) == 2:
            return True
        else:
            logger.error('%s: %s'.response.status_code, response.text)
        return False

    def device_delete(self, tenant, device):
        url = 'http://{}:28080/registration/{}/{}'.format(self.addr, tenant, device)
        response = requests.delete(url)

        if int(response.status_code//100) == 2:
            return True
        else:
            logger.error('%s: %s', response.status_code, response.text)
        return False

    def credentials_create(self, tenant, device, login, password):
        url = 'http://{}:28080/credentials/{}'.format(self.addr, tenant)
        response = requests.post(url, json={
            'device-id': device,
            'type': 'hashed-password',
            'auth-id': login,
            'secrets': [{'pwd-plain': password}]})

        if int(response.status_code//100) == 2:
            return True
        else:
            logger.error('%s: %s', response.status_code, response.text)
        return False

    def credentials_create(self, tenant, device, login, password):
        url = 'http://{}:28080/credentials/{}/{}'.format(self.addr, tenant, device)
        response = requests.delete(url)

        if int(response.status_code//100) == 2:
            return True
        else:
            logger.error('%s: %s', response.status_code, response.text)
        return False

#hono = Hono()
#tenant = 'demo'
#device = 'laptop'
#print(hono.tenant_create('demo'))
