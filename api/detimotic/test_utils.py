import unittest
import datetime
import utils

class TestUtils(unittest.TestCase):
    
    def test_json(self):
        j = '{ "temperature":23.60,"humidity":52.70,"light":186,"sound":561 }'
        self.assertTrue(utils.is_json(j))

    def test_keys(self):
        j = '{ "temperature":23.60,"humidity":52.70,"light":186,"sound":561 }'
        res = ['["temperature"]', '["humidity"]', '["light"]', '["sound"]'] 
        self.assertEqual(utils.json_to_keys(j), res)
    
    def test_json_to_points(self):
        now = datetime.datetime.now()
        j='{ "temperature":23.60,"humidity":52.70,"light":186,"sound":561 }'
        res=[{'measurement': 'temperature',
        'tags': {'queue': 'event', 'tenant': 'demo', 'device': 'test', 'mapper': '0.2'},
        'time': now.isoformat(),
        'fields': {'temperature': 23.60}},
        {'measurement': 'humidity',
        'tags': {'queue': 'event', 'tenant': 'demo', 'device': 'test', 'mapper': '0.2'},
        'time': now.isoformat(),
        'fields': {'humidity': 52.70}},
        {'measurement': 'light',
        'tags': {'queue': 'event', 'tenant': 'demo', 'device': 'test', 'mapper': '0.2'},
        'time': now.isoformat(),
        'fields': {'light': 186}},
        {'measurement': 'sound',
        'tags': {'queue': 'event', 'tenant': 'demo', 'device': 'test', 'mapper': '0.2'},
        'time': now.isoformat(),
        'fields': {'sound': 561}}]
        self.assertEqual(utils.json_to_points('event', 'demo', 'test', now, j), res)
    
    def test_json_to_features(self):
        j='{ "temperature":23.60,"humidity":52.70,"light":186,"sound":561 }'
        res={'temperature': {'properties': {'value': None}},
        'humidity': {'properties': {'value': None}},
        'light': {'properties': {'value': None}},
        'sound': {'properties': {'value': None}}}
        self.assertEqual(utils.json_to_features(j), res)
    
    def test_json_to_function(self):
        j='{"humidity":61.82,"linkquality":28,"temperature":22.02,"pressure":1005.7,"battery":97,"voltage":2995}'
        res='''function mapToDittoProtocolMsg(headers, textPayload, bytePayload, contentType) {
    var jsonData;
    if (contentType == "application/json"){
        jsonData = JSON.parse(textPayload);
    } else  {
        var payload = Ditto.asByteBuffer(bytePayload);
        jsonData = JSON.parse(payload.toUTF8());
    }
    value = {"humidity": {"properties": {"value": jsonData["humidity"]}},"linkquality": {"properties": {"value": jsonData["linkquality"]}},"temperature": {"properties": {"value": jsonData["temperature"]}},"pressure": {"properties": {"value": jsonData["pressure"]}},"battery": {"properties": {"value": jsonData["battery"]}},"voltage": {"properties": {"value": jsonData["voltage"]}}};
    return Ditto.buildDittoProtocolMsg("demo", headers["device_id"], "things", "twin", "commands", "modify", "/features", headers, value);
    }'''
        #print(utils.json_to_function('demo', j))
        self.assertEqual(utils.json_to_function('demo', j), res)

if __name__ == '__main__':
    unittest.main()
