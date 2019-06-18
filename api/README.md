#DETIMotic API

Python library that contains several wrappers for the DETIMotic platform.
Furthermore, it contains methods to automatically map any JSON into InFluxDB data points and Ditto Incoming Mapping function.

## Automatic Mapping Methods

[JSON](http://json.org/) was selected as the primary representation for data sharing.
It was been widely used in IoT and HTML scenarios.
A JSON Object is a recursive dictionary, each entry of the dictionary can contains another valid dictionary.
However, we do not want to force a schema on the users sharing data with the platform.
As such, two automatic methods were developed to parse and map any valid JSON into the necessary structures.

It is important to mention that the method developed where was inspired by the mapping rules implemented by [Telegraph](https://www.influxdata.com/time-series-platform/telegraf/).

### HONO

Does not require any mapping function.

### Cassandra

Does not require any mapping function.

### InfluxDB

InfluxDB data model is based on measurements, tags and fields.
**Measurements** represent physical attributes (such as temperature, humidity, etc.).
Can be seen as a database of sorts in Relational models
**Tags** and **Fields** are similar to relational columns with tags being indexed, while fields are not indexed.

The mapping functions flats the JSON Object into a single dictionary (non-recursive) as such:

```json
{
    "indoor":{
        "temperature":25,
        "humidity":0.6
    },
    "outdoor":{
        "temperature":18,
        "humidity":0.5
    }
}
```

Into:

```json
{
    "indoor.temperature":25,
    "indoor.humidity":0.6,
    "outdoor.temperature":18,
    "outdoor.humidity":0.5
}
```

After this transformation it is simpler to convert the document into data points:
1. Each line of the document is considered a measurement
2. The tags are the topic, tenant, device and mapper version (for more information regarding Hono topic, tenant and device check [here](../setup/README.md)).
3. The field are again each line of the object with the corresponding value.

### Ditto

Ditto allows one to create virtual things that are virtual counterparts to real sensors.
They allow the devices to be exposed through Web APIs such as REST and WebSockets.
However, the internal structure of the virtual device is quite rigid.

Our mapping solution is similar to the previous one.
It transforms a JSON Object into a flat hierarchy.

After that is creates a Ditto virtual device:

```json
{
    "temperature":23.60,
    "humidity":52.70,
    "light":186,
    "sound":561
}
```

Into:

```json
{
    "temperature": {"properties": {"value": null}},
    "humidity": {"properties": {"value": null}},
    "light": {"properties": {"value": null}},
    "sound": {"properties": {"value": null}}
}
```

And also creates a mapping function in JavaScript (Ditto requirement) with the following code:

```javascript
function mapToDittoProtocolMsg(headers, textPayload, bytePayload, contentType) {
    var jsonData;
    
    if (contentType == "application/json"){
        jsonData = JSON.parse(textPayload);
    } else  {
        var payload = Ditto.asByteBuffer(bytePayload);
        jsonData = JSON.parse(payload.toUTF8());
    }
    
    value = {"temperature": {"properties": {"value": jsonData["temperature"]}},
    "humidity": {"properties": {"value": jsonData["humidity"]}},
    "light": {"properties": {"value": jsonData["light"]}},
    "sound": {"properties": {"value": jsonData["sound"]}}};
    
    return Ditto.buildDittoProtocolMsg("demo", headers["device_id"], "things", "twin", "commands", "modify", "/features", headers, value);
    }
```

## Setup

In order to install this library simply run:

```console
pip install api
```

If you need to install this library into some virtual environment:

```console
pip install <path to here>
```