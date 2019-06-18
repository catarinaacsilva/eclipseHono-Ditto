#!/bin/bash

USER="consumer@HONO"
PASSWORD="verysecret"
HONO_SERVER="192.168.85.107"
DITTO_SERVER="192.168.85.204"

echo "Please enter Tenant ID:"
read TENANT_ID
echo "Your Tenant ID entered: $TENANT_ID"
echo "Please enter Device ID:"
read DEVICE_ID
echo "Your Device ID entered: $DEVICE_ID"

# isnerir no terminal a função de mapeamento
#echo "Insert Mapping Funcion (convert JSON from Hono to Ditto JSON structure):"
#read MAPPING_FUNCTION

# importar um ficheiro com a função de mapeamento (o ficheiro nao precisa de ter extensao)
echo "insert path to file with Mapping Function: "
read input
while IFS= read -r var
do
  MAPPING_FUNCTION=$var
done < "$input"

echo "Hono - Register tenant"
curl -i -X POST -H 'Content-Type: application/json' -d '{"tenant-id":"$TENANT_ID"}' http://HONO_SERVER:28080/tenant/

echo "Hono - Register device"
curl -i -X POST -H 'Content-Type: application/json' -d '{"device-id":"$DEVICE_ID"}' http://HONO_SERVER:28080/registration/$TENANT_ID #mudar este demo
# Ditto - Verify connection and mapping
curl -X POST -i -H 'Content-Type: application/json' -d '{"device-id": "$DEVICE_ID","type": "hashed-password","auth-id": "sensor-auth","secrets": [{"hash-function" : "sha-512","pwd-hash": "sQnzu7wkTrgkQZF+0G1hi5AI3Qmzvv0bXgc5THBqi7mAsdd4Xll27ASbRt9fEyavWi6m0QP9B8lThf+rDKy8hg=="}]}' http://HONO_SERVER:28080/credentials/TENANT_ID

# Ditto - Register TENANT_ID:sensor virtual device
echo "Ditto - Register $TENANT_ID"
curl -X PUT -i -u detimotic:detimotic -H 'Content-Type: application/json' -d '{"attributes": {"location": "DETI"},"features": {"temperature": {"properties": {"value": null}},"rpm": {"properties": {"value": null}}}}' http://DITTO_SERVER:8080/api/2/things/$TENANT_ID:$DEVICE_ID

echo "Ditto - Test connection with Hono"
curl -X POST -i -u devops:foobar -H 'Content-Type: application/json' -d '{
    "targetActorSelection": "/system/sharding/connection",
    "headers": {
        "aggregate": false
    },
    "piggybackCommand": {
        "type": "connectivity.commands:testConnection",
        "connection": {
            "id": "hono-sensor",
            "connectionType": "amqp-10",
            "connectionStatus": "open",
            "uri": "amqp://consumer%40HONO:PASSWORD@SERVER15672",
            "failoverEnabled": true,
            "sources": [{
                "addresses": [
                    "telemetry/$TENANT_ID",
                    "event/$TENANT_ID"
                ],
                "authorizationContext": ["nginx:detimotic"]
            }]
        }
    }
}' http://DITTO_SERVER:8080/devops/piggyback/connectivity?timeout=8000


echo "Ditto - Add mapping function"
curl -X POST -i -u devops:foobar -H 'Content-Type: application/json' -d '{
    "targetActorSelection": "/system/sharding/connection",
    "headers": {
        "aggregate": false
    },
    "piggybackCommand": {
        "type": "connectivity.commands:createConnection",
        "connection": {
            "id": "hono-sensor",
            "connectionType": "amqp-10",
            "connectionStatus": "open",
            "uri": "amqp://consumer%40HONO:PASSWORD@HONO_SERVER:15672",
            "failoverEnabled": true,
            "sources": [{
                "addresses": [
                    "telemetry/$TENANT_ID",
                    "event/$TENANT_ID"
                ],
                "authorizationContext": ["nginx:detimotic"]
            }],
        "mappingContext": {
                "mappingEngine": "JavaScript",
                "options": {"loadBytebufferJS":true,"loadLongJS":true,
"incomingScript": $MAPPING_FUNCTION #inserir aqui a função de mapeamento pq so isto tinha info sobre temperatura (que era especifico)
            }
        }
    }
}' http://DITTO_SERVER:8080/devops/piggyback/connectivity?timeout=8000


echo "Ditto - Verify connection and mapping"
curl -X POST -i -u devops:foobar -H 'Content-Type: application/json' -d '{
    "targetActorSelection": "/system/sharding/connection",
    "headers": {
        "aggregate": false
    },
    "piggybackCommand": {
        "type": "connectivity.commands:retrieveConnectionMetrics",
        "connectionId": "hono-sensor"
    }
}' http://DITTO_SERVER:8080/devops/piggyback/connectivity?timeout=8000