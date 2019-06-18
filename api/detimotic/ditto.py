# coding: utf-8


__author__ = 'Catarina Silva'
__version__ = '0.3'
__email__ = 'c.alexandracorreia@ua.pt'
__status__ = 'Development'


import json
import logging
import requests
from requests.auth import HTTPBasicAuth
from .utils import json_to_features, json_to_function


#logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',datefmt='%m-%d %H:%M:%S')
logger = logging.getLogger('DITTO API')


class Ditto:
    def __init__(self, addr='192.168.85.204', user='detimotic', password='detimotic', dev_user='devops', dev_password='foobar'):
        self.addr = addr
        self.user = user
        self.password = password
        self.dev_user = dev_user
        self.dev_password = dev_password

    def thing_create(self, tenant, device, attributes={}, features={}):
        url = 'http://{}:8080/api/2/things/{}:{}'.format(self.addr, tenant, device)
        j = {'thingId':'{}:{}'.format(tenant, device), 'policyId':'{}:{}'.format(tenant, device), 'attributes': attributes, 'features': features}
        #j = {'thingId':'{}:{}'.format(tenant, device), 'attributes': attributes, 'features': features}
        response = requests.put(url, json=j,auth=HTTPBasicAuth(self.user, self.password))

        if int(response.status_code//100) == 2:
            return True
        else:
            logger.error('thing_create %s: %s', response.status_code, response.text)
            logger.error('%s', j)
        return False
    
    def thing_delete(self, tenant, device):
        url = 'http://{}:8080/api/2/things/{}:{}'.format(
            self.addr, tenant, device)
        response = requests.delete(url,
        auth=HTTPBasicAuth(self.user, self.password))

        if int(response.status_code//100) == 2:
            return True
        else:
            logger.error('%s: %s', response.status_code, response.text)
        return False

    def thing_exists(self, tenant, device):
        url = 'http://{}:8080/api/2/things/{}:{}'.format(self.addr, tenant, device)
        response = requests.get(url,
        auth=HTTPBasicAuth(self.user, self.password))

        if int(response.status_code//100) == 2:
            return True
        else:
            logger.error('thing_exists %s: %s', response.status_code, response.text)
        return False

    def thing_exists_empty(self, tenant, device):
        url = 'http://{}:8080/api/2/things/{}:{}/features'.format(self.addr, tenant, device)
        response = requests.get(url,
        auth=HTTPBasicAuth(self.user, self.password))

        if int(response.status_code//100) == 2:
            data = json.loads(response.text)
            if not data:
                return True
        else:
            logger.error('%s: %s', response.status_code, response.text)
        return False

    def thing_update_features(self, tenant, device, json):
        url = 'http://{}:8080/api/2/things/{}:{}/features'.format(
            self.addr, tenant, device)
        response = requests.put(url,
        json=json_to_features(json),
        auth=HTTPBasicAuth(self.user, self.password))

        if int(response.status_code//100) == 2:
            return True
        else:
            logger.error('%s: %s', response.status_code, response.text)
        return False
    
    # Not fully implemented...
    def thing_search(self):
        items = []
        '''
        {"items":[{"thingId":"demo:test","policyId":"demo:test","attributes":{},"features":{"temperature":{"properties":{"value":null}},"humidity":{"properties":{"value":null}}}}],"nextPageOffset":-1}
        '''
        #while not done:
        url = 'http://{}:8080/api/2/search/things'.format(self.addr)
        response = requests.get(url,auth=HTTPBasicAuth(self.user, self.password))

        if int(response.status_code//100) == 2:
            print(response.text)
            return items
        else:
            logger.error('%s: %s', response.status_code, response.text)
        return False
    
    def policies_create(self, policy, user='detimotic'):
        url = 'http://{}:8080/api/2/policies/{}'.format(self.addr, policy)
        j={'entries':{
            'owner' : {
                'subjects': {
                    'nginx:{}'.format(user):{
                        'type': 'nginx basic auth user'}
                    },
                'resources':{
                    'things:/':{'grant':['READ', 'WRITE'], 'revoke':[]},
                    'policy:/':{'grant':['READ', 'WRITE'], 'revoke':[]},
                    'message:/':{'grant':['READ', 'WRITE'], 'revoke':[]}}
                }
            }
        }
        response = requests.put(url, json=j, auth=HTTPBasicAuth(self.user, self.password))

        if int(response.status_code//100) == 2:
            return True
        else:
            logger.error('%s: %s', response.status_code, response.text)
        return False

    def policies_delete(self, policy):
        url = 'http://{}:8080/api/2/policies/{}'.format(self.addr, policy)
        response = requests.delete(url, auth=HTTPBasicAuth(self.user, self.password))

        if int(response.status_code//100) == 2:
            return True
        else:
            logger.error('%s: %s', response.status_code, response.text)
        return False

    def devops_piggyback_create_hono_mapping(self, tenant, device, uri, json, user='detimotic'):
        url = 'http://{}:8080/devops/piggyback/connectivity?timeout=8000'.format(self.addr)
        function = json_to_function(tenant, json)
        json = {'targetActorSelection': '/system/sharding/connection',
                'headers': {'aggregate': False},
                'piggybackCommand': {
                    'type': 'connectivity.commands:createConnection',
                    'connection': {
                        'id': 'hono-{}-{}'.format(tenant, device),
                        'connectionType': 'amqp-10',
                        'connectionStatus': 'open',
                        'uri': uri,  # "amqp://consumer%40HONO:verysecret@192.168.85.107:15672",
                        'failoverEnabled': True,
                        'sources': [{
                            'addresses': ['event/{}'.format(tenant)],
                            'authorizationContext': ['nginx:{}'.format(user)]}],
                        'mappingContext': {
                            'mappingEngine': "JavaScript",
                            'options': {
                                'loadBytebufferJS': True,
                                'loadLongJS': True,
                                'incomingScript': function
                        }
                    }
                }
            }
        }

        response = requests.post(url,
        json=json, auth=HTTPBasicAuth(self.dev_user, self.dev_password))

        if int(response.status_code//100)  == 2:
            return True
        else:
            logger.error('%s: %s', response.status_code, response.text)
        return False
        
    
    def devops_piggyback_delete_hono_mapping(self, tenant, device):
        url = 'http://{}:8080/devops/piggyback/connectivity?timeout=8000'.format(self.addr)
        json = {'targetActorSelection': '/system/sharding/connection',
        'headers': {'aggregate': False},
        'piggybackCommand': {
        'type': 'connectivity.commands:deleteConnection',
        'connectionId': 'hono-{}-{}'.format(tenant, device)}}

        response = requests.post(url,
        json=json, auth=HTTPBasicAuth(self.dev_user, self.dev_password))

        if int(response.status_code//100)  == 2:
            return True
        else:
            logger.error('%s: %s', response.status_code, response.text)
        return False


#ditto = Ditto('192.168.85.211', 'ditto', 'ditto')
#ditto = Ditto()
#tenant = 'demo'
#device = 'laptop'
#policy = 'detimotic:detimotic'
#j={'temperature':25.0, 'humidity':0.65}
#print(ditto.policies_delete(tenant, device))
#print(ditto.thing_create(tenant, device, {}, json_to_features(j)))
#print(ditto.devops_piggyback_create_hono_mapping(tenant, device, 'amqp://consumer%40HONO:verysecret@192.168.85.107:15672', j))
#print(ditto.devops_piggyback_delete_hono_mapping(tenant, device))
#print(ditto.policies_create(policy))
#print(ditto.thing_search())
#print(ditto.thing_delete(tenant, device))