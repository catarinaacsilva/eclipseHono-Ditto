# coding: utf-8


__author__ = 'Catarina Silva'
__version__ = '0.2'
__email__ = 'c.alexandracorreia@ua.pt'
__status__ = 'Development'


import logging
from flask import Flask
from flask import request
from flask import render_template
from detimotic.ditto import Ditto
from detimotic.utils import Cache, json_to_features


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('MGT_PORTAL')


URI='amqp://consumer%40HONO:verysecret@192.168.85.107:15672'


app = Flask(__name__)
cache = Cache()
ditto = Ditto()


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/map',  methods=['POST'])
def map():
    if request.is_json:
        content = request.get_json()
        tenant = content['tenant']
        device = content['device']
        j = content['json']
        key = (tenant, device)

        logger.info('Map the following device %s:%s = %s', tenant, device, j)
        
        if key not in cache:
            logger.info('Device %s:%s not in cache...', tenant, device)
            if not ditto.thing_exists(tenant, device):
                logger.info('Device %s:%s  does not exists in Ditto...', tenant, device)
                rv = ditto.thing_create(tenant, device,
                {'tenant':tenant, 'device':device, 'mapper':__version__},
                json_to_features(j))
                logger.info('Create device = %s', rv)
                rv = ditto.devops_piggyback_create_hono_mapping(tenant, device, URI, j)
                logger.info('Map device = %s', rv)
                cache.update(key, True)
            else:
                logger.info('Device %s:%s already exists in Ditto', tenant, device)
        else:
            logger.info('Device %s:%s in cache...', tenant, device)
    return '200 OK'


if __name__ == "__main__":
    app.run(host='0.0.0.0')
