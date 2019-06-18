# Demo #1

Basic demo that showcases the potential of the DETIMotic platform.
This demo connects the following components:
1. Python script that reads CPU load
2. Hono (Broker)
3. Ditto (Virtual Things)
5. Dashboard

![alt text](html/images/demo01.png)

## Access to the services

For more information regarding connection please read [here](../setup/README.md)
 
## Run the demo

```console
./start.sh
```

### Setup the demo (APIs)

In [here](../api) you can find python APIs to create devices and virtual things.
Furthermore the [Management Portal](../mgt_portal/README.md) is responsible for automatically mapping the physical devices into virtual things.

### Setup the demo (Manually)

#### Hono - Register tenant: demo

```console
curl -i -X POST -H 'Content-Type: application/json' -d '{"tenant-id":"demo"}' http://192.168.85.107:28080/tenant/
```

#### Hono - Register device: laptop 

```console
curl -i -X POST -H 'Content-Type: application/json' -d '{"device-id":"laptop"}' http://192.168.85.107:28080/registration/demo
```

## Add hashed password do laptop device with auth-id laptop-auth

```console
curl -X POST -i -H 'Content-Type: application/json' -d '{"device-id": "laptop","type": "hashed-password","auth-id": "laptop-auth","secrets": [{"hash-function" : "sha-512","pwd-hash": "sQnzu7wkTrgkQZF+0G1hi5AI3Qmzvv0bXgc5THBqi7mAsdd4Xll27ASbRt9fEyavWi6m0QP9B8lThf+rDKy8hg=="}]}' http://192.168.85.107:28080/credentials/demo
```

#### Ditto - Register demo:laptop virtual device

```console
curl -X PUT -i -u detimotic:detimotic -H 'Content-Type: application/json' -d '{"attributes": {"location": "DETI"},"features": {"temperature": {"properties": {"value": null}},"rpm": {"properties": {"value": null}}}}' http://192.168.85.204:8080/api/2/things/demo:laptop
```

#### Ditto - Test connection with Hono

```console
curl -X POST -i -u devops:foobar -H 'Content-Type: application/json' -d '{
    "targetActorSelection": "/system/sharding/connection",
    "headers": {
        "aggregate": false
    },
    "piggybackCommand": {
        "type": "connectivity.commands:testConnection",
        "connection": {
            "id": "hono-demo-laptop",
            "connectionType": "amqp-10",
            "connectionStatus": "open",
            "uri": "amqp://consumer%40HONO:verysecret@192.168.85.107:15672",
            "failoverEnabled": true,
            "sources": [{
                "addresses": [
                    "telemetry/demo",
                    "event/demo"
                ],
                "authorizationContext": ["nginx:detimotic"]
            }]
        }
    }
}' http://192.168.85.204:8080/devops/piggyback/connectivity?timeout=8000
```

#### Ditto - Add mapping function (convert JSON from Hono to Ditto JSON structure)

```console
curl -X POST -i -u devops:foobar -H 'Content-Type: application/json' -d '{
    "targetActorSelection": "/system/sharding/connection",
    "headers": {
        "aggregate": false
    },
    "piggybackCommand": {
        "type": "connectivity.commands:createConnection",
        "connection": {
            "id": "hono-demo-laptop",
            "connectionType": "amqp-10",
            "connectionStatus": "open",
            "uri": "amqp://consumer%40HONO:verysecret@192.168.85.107:15672",
            "failoverEnabled": true,
            "sources": [{
                "addresses": [
                    "telemetry/demo",
                    "event/demo"
                ],
                "authorizationContext": ["nginx:detimotic"]
            }],
        "mappingContext": {
                "mappingEngine": "JavaScript",
                "options": {"loadBytebufferJS":true,"loadLongJS":true,
"incomingScript": "function mapToDittoProtocolMsg(headers, textPayload, bytePayload, contentType) {\n var jsonData;\n if (contentType == \"application/json\") { jsonData = JSON.parse(textPayload); }\n else  {\n var payload = Ditto.asByteBuffer(bytePayload);\n jsonData = JSON.parse(payload.toUTF8()); }\n value = {temperature: {properties: {value: jsonData.temp}},rpm: {properties: {value: jsonData.rpm}}};\n return Ditto.buildDittoProtocolMsg(\"demo\", headers[\"device_id\"], \"things\", \"twin\", \"commands\", \"modify\", \"/features\", headers, value);\n }"}
            }
        }
    }
}' http://192.168.85.204:8080/devops/piggyback/connectivity?timeout=8000
```

#### Ditto - Verify connection and mapping

```console
curl -X POST -i -u devops:foobar -H 'Content-Type: application/json' -d '{
    "targetActorSelection": "/system/sharding/connection",
    "headers": {
        "aggregate": false
    },
    "piggybackCommand": {
        "type": "connectivity.commands:retrieveConnectionMetrics",
        "connectionId": "hono-demo-laptop"
    }
}' http://192.168.85.204:8080/devops/piggyback/connectivity?timeout=8000
```

#### Remove connection (only on bugs are found)

```console
curl -X POST -i -u devops:foobar -H 'Content-Type: application/json' -d '{
    "targetActorSelection": "/system/sharding/connection",
    "headers": {
        "aggregate": false
    },
    "piggybackCommand": {
        "type": "connectivity.commands:deleteConnection",
        "connectionId": "hono-demo-laptop"
    }
}' http://192.168.85.204:8080/devops/piggyback/connectivity?timeout=8000
```


#### Other

[HONO api](https://www.eclipse.org/hono/api/)

[DITTO api](https://www.eclipse.org/ditto/http-api-doc.html#/Things)

```console
curl -i -X GET http://192.168.85.107:28080/tenant/<TENANT-ID>
```

```console
curl -i -X GET http://192.168.85.107:28080/registration/<TENANT-ID>/<DEVICE-ID>
```
