# coding: utf-8

__author__ = 'Catarina Silva'
__version__ = '0.2'
__email__ = 'c.alexandracorreia@ua.pt'
__status__ = 'Development'


import json
import random
import logging
import datetime
import threading
import statistics

	
def synchronized(func):
	
    func.__lock__ = threading.Lock()
		
    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)

    return synced_func


class Cache:
    
    def __init__(self, max_cache_size=30):
        self.cache = {}
        self.max_cache_size = max_cache_size
    
    @synchronized
    def __contains__(self, key):
        """
        Returns True or False depending on whether or not the key is in the 
        cache
        """
        if key in self.cache:
            value = self.cache[key]['value']
            self.cache[key] = {'date_accessed': datetime.datetime.now(), 'value': value}
            return True
        return False
 
    @synchronized
    def update(self, key, value):
        """
        Update the cache dictionary and optionally remove the oldest item
        """
        if key not in self.cache and len(self.cache) >= self.max_cache_size:
            self.remove_oldest()
 
        self.cache[key] = {'date_accessed': datetime.datetime.now(), 'value': value}
 
    @synchronized
    def remove_oldest(self):
        """
        Remove the entry that has the oldest accessed date
        """
        oldest_entry = None
        for key in self.cache:
            if oldest_entry is None:
                oldest_entry = key
            elif self.cache[key]['date_accessed'] < self.cache[oldest_entry]['date_accessed']:
                oldest_entry = key
        self.cache.pop(oldest_entry)
 
    @property
    def size(self):
        """
        Return the size of the cache
        """
        return len(self.cache)


def is_json(txt):
    try:
        json_object = json.loads(txt)
    except:
        return False
    return True


def is_list_numeric(lst):
    if isinstance(lst, list):
        return all(isinstance(x, (int, float)) for x in lst)
    return False


def is_list_str(lst):
    if isinstance(lst, list):
        return all(isinstance(x, (str)) for x in lst)
    return False


def is_list_dict(lst):
    if isinstance(lst, list):
        return all(isinstance(x, (dict)) for x in lst)
    return False


def new_prefix(prefix, key):
    if not prefix:
        return str(key)
    return '%s.%s'%(prefix, key)


def flat_dict(data, prefix=''):
    stack = [(data, prefix)]
    flat = {}

    while stack:
        d, p = stack.pop()
        for key in d.keys():
            value = data[key]
            if isinstance(value, dict):
                stack.append((value, new_prefix(p, key)))
            else:
                if isinstance(value, int):
                    value = float(value)
                flat[new_prefix(prefix, key)] = value
    return flat


def flat_json(j):
    d = json.loads(j)
    return flat_dict(d)


def json_to_points(queue, tenant, device, timestamp, data, points=[], prefix=''):
    flat = flat_json(data)
    for key in flat.keys():
        value = flat[key]
        if is_list_numeric(value):
            avg = statistics.mean(value)
            std = statistics.stdev(value)
            json_body = {'measurement': key,
                'tags':{'queue': queue, 'tenant': tenant, 'device': device, 'mapper': __version__},
                'time': timestamp.isoformat(),'fields': {'{}.avg'.format(key): avg, '{}.std'.format(key): std}}
            points.append(json_body)
        elif is_list_dict(value):
            for d in value:
                json_to_points(queue, tenant, device, timestamp, d, points, key)
        elif not isinstance(value, list):
            json_body = {'measurement': key,
                'tags':{'queue': queue, 'tenant': tenant, 'device': device, 'mapper': __version__},
                'time': timestamp.isoformat(),'fields': {key: value}}
            points.append(json_body)
    return points


def json_to_features(j):
    if is_json(j):
        flat = flat_json(j)
    else:
        flat = flat_dict(j)
    rv = {}
    for key in flat.keys():
        rv[key]={'properties':{'value':None}}
    return rv


def json_to_keys(j):
    d = json.loads(j)
    return dict_to_keys(d)


def dict_to_keys(data, prefix=''):
    stack = [(data, prefix)]
    keys=[]

    while stack:
        d, p = stack.pop()
        for k in d.keys():
            key='["{}"]'.format(k)
            if isinstance(data[k], dict):
                stack.append((value, '{}{}'.format(p, key)))
            else:
                keys.append('{}{}'.format(p, key))
    return keys


def json_to_function(tenant, j):
    if is_json(j):
        keys = json_to_keys(j)
    else:
        keys = dict_to_keys(j)
    values = []
    if len(keys) > 0:
        for i in range(len(keys)-1):
            values.append('"{0}": {{"properties": {{"value": jsonData{1}}}}},'.format(keys[i][2:-2], keys[i]))
        values.append('"{0}": {{"properties": {{"value": jsonData{1}}}}}'.format(keys[-1][2:-2], keys[-1]))
        values = '{{{0}}}'.format(''.join(values))

    function = '''function mapToDittoProtocolMsg(headers, textPayload, bytePayload, contentType) {{
    var jsonData;
    if (contentType == "application/json"){{
        jsonData = JSON.parse(textPayload);
    }} else  {{
        var payload = Ditto.asByteBuffer(bytePayload);
        jsonData = JSON.parse(payload.toUTF8());
    }}
    value = {0};
    return Ditto.buildDittoProtocolMsg("{1}", headers["device_id"], "things", "twin", "commands", "modify", "/features", headers, value);
    }}'''.format(values, tenant)

    return function
