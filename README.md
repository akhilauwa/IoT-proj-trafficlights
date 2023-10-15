# IoT-proj-trafficlights

### Virtual Environment
It is recommended to use a virtual environment to run this project. To create a virtual environment, run the following command in the project directory:
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

### Running the python script at RPi Startup
In the terminal type:
```
sudo nano /etc/rc.local
```
Before exit 0, insert:
```
sudo bash ~/Documents/IoT-proj-trafficlights/start_traffic.sh &
```
Note that start_traffic.sh needs to be in the IoT-proj-trafficlights directory