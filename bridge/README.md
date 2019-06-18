# Bridge (Hono <-> Storage)

The bridge connects the Hono to the persistent storage.
In order to fully comprehend the architecture of the DETIMotic platform see [here](../setup/README.md).

## Setup

In order to setup the bridge, for the first time, please run the following commands.
First, follow the steps necessary to have access to the storage machine (or the machine where the bridge will be running).

```console
ssh storage
mkdir git
cd git
git clone  https://code.ua.pt/git/pei-2018-2019-g12
cd pei-2018-2019-g12/servers/bridge
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
pip3 install ../api/
deactivate
sudo cp -vf bridge.service /etc/systemd/system/
sudo systemctl unmask bridge
sudo systemctl enable bridge
sudo systemctl start bridge
```

In order to update the code of the bridge, just run the following commands:

```console
sudo systemctl stop bridge
cd git/pei-2018-2019-g12/servers/bridge
source venv/bin/activate
git pull
pip3 install --upgrade -r requirements.txt
pip3 install --upgrade ../api/
deactivate
sudo cp -vf bridge.service /etc/systemd/system/
sudo systemctl unmask bridge
sudo systemctl enable bridge
sudo systemctl start bridge
```
