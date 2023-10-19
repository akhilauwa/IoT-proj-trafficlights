# IoT-proj-trafficlights

## Running Traffic Login on Raspberry Pi
The Raspberry Pi must run the smart_controller.py script in the V1 folder:
```
python smart_controller.py
```

## Running YOLO on the Server

### Virtual Environment
It is recommended to use a virtual environment to run this project on the server. To create a virtual environment, run the following command in the project directory:
```
python -m venv venv
```
To activate the virtual environment, run one of the following commands depending on your operating system:
```
source venv/bin/activate    # Linux or macOS
venv/Scripts/activate       # Windows
```
To deactivate the virtual environment, run the following command:
```
deactivate
```

The server must run the wifi_server.py script in the V1 folder:
```
python wifi_server.py
```

## Running the python script at RPi Startup
In the terminal type:
```
sudo nano /etc/rc.local
```
Before exit 0, insert (modify [USERNAME] to the RPi username):
```
sudo bash /home/[USERNAME]/Documents/IoT-proj-trafficlights/start_traffic.sh &
```
Modify [USERNAME] in start_traffic.sh line 1:
```
cd /home/[USERNAME]/Documents/IoT-proj-trafficlights
```
Note that start_traffic.sh may need execute permissions, navigate to its location and type:
```
chmod +x start_traffic.sh
```
