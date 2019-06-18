# Management Portal

The **mgt_portal** is responsible for mapping real devices into virtual things.
Furthermore, it should be used to manage virtual and real sensors (not fully implemented).

## Setup

The portal was devised using [Flask](http://flask.pocoo.org/) and [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/).
The webservice is deployed into [NGINX](https://www.nginx.com/).
The deployment follow the instructions in this [website](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04).

### Creating a systemd Unit File

```console
sudo cp -vf mgt_portal.service /etc/systemd/system/
sudo systemctl enable mgt_portal
sudo systemctl start mgt_portal
```

### Configuring Nginx to Proxy Requests

```console
sudo apt install nginx-light
sudo nano /etc/nginx/sites-available/mgt_portal
```

Add the following configuration:

```text
server {
    listen 80;
    server_name detimotic www.detimotic;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/detimotic/git/pei-2018-2019-g12/servers/mgt_portal/mgt_portal.sock;
    }
}
```

To enable the Nginx server block configuration you've just created, link the file to the sites-enabled directory:

```console
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/mgt_portal /etc/nginx/sites-enabled
```

With the file in that directory, we can test for syntax errors by typing:

```console
sudo nginx -t
```

If this returns without indicating any issues, restart the Nginx process to read the new configuration:

```console
sudo systemctl restart nginx
```

## Manual Device Management

Tenants are used to groups devices together, and ease the burden of management.
If the devices do not have enough resources to deal with the API provided by Hono,
they can use a gateway to forward the data.
Nevertheless, the gateway is optional.

The devices have feedback from the platform regarding the whether the data is 
accepted or not. The main reasons for a refused message are: invalid authentication,
wrong topic or tenant or event a missing consumer (for the Telemetry queue).

Before sending data to the platform it is necessary to create a tenant and a device.

### Tenants (Hono)

#### Create a Tenant

```conole
curl -i -X POST -H 'Content-Type: application/json' -d '{
"tenant-id":<TENANT>
}' http://192.168.85.107:28080/tenant/
```

#### Remove a Tenant

```conole
curl -i -X DELETE http://192.168.85.107:28080/tenant/<TENANT>
```

#### Get Tenant information

```conole
curl -i -X GET http://192.168.85.107:28080/tenant/<TENANT>
```

### Devices (Hono)

#### Create a Device

```conole
curl -i -X POST -H 'Content-Type: application/json' -d '{
    "device-id": <DEVICE>
}'  http://192.168.85.107:28080/registration/<TENANT>
```

#### Remove a Device

```conole
curl -i -X DELETE http://192.168.85.107:28080/registration/<TENANT>/<DEVICE>
```

#### Get Device information

```conole
curl -i -X GET http://192.168.85.107:28080/registration/<TENANT>/<DEVICE>
```

### Device Credentials (Hono):

#### Create Credentials for a Device:

```console
curl -i -X POST -H 'Content-Type: application/json' --d '{
  "device-id": <DEVICE>,
  "type": "hashed-password",
  "auth-id": <DEVICE_LOGIN>,
  "secrets": [{
      "pwd-plain": <PASSWORD>
  }]
}' http://192.168.85.107:28080/credentials/<TENANT>
```

#### Remove Device Credentials:

```console
curl -i -X DELETE http://192.168.85.107:28080/credentials/<TENANT>/<DEVICE>
```

### Register a digital twin (Ditto):

```console
curl -X PUT -i -u detimotic:detimotic -H 'Content-Type: application/json' -d '{
"attributes": {"location": "DETI"},
"features": {
"temperature": 
{"properties": {"value": null}},
"rpm": 
{"properties": {"value": null}}}
}' http://192.168.85.204:8080/api/2/things/<TENANT>:<DEVICE>
```

### Connect Hono device with Ditto digital twin

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
                    "telemetry/<TENANT>",
                    "event/<TENANT>"
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

## Further Information

[Hono Device Registry](https://www.eclipse.org/hono/user-guide/device-registry/)

[Ditto API](https://www.eclipse.org/ditto/http-api-doc.html)

[Connect Hono with Ditto](https://www.eclipse.org/ditto/2018-05-02-connecting-ditto-hono.html)

[Ditto Command and Control](https://www.eclipse.org/ditto/2018-12-05-example-command-and-control.html)