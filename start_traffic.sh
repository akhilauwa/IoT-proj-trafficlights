# This script is run on startup of the Raspberry Pi.

cd /home/[USERNAME]/Documents/IoT-proj-trafficlights

source venv/bin/activate

echo "venv activated." >> ../trafficlights.log

while ! ping -c 1 google.com &>/dev/null; do
	sleep 5
done

echo "Internet connected." >> ../trafficlights.log

# sudo python thread_smart_lights.py
sudo python V1/smart_controller.py

# This line should not be reached (script is an infinite loop)
echo "Python script running." >> ../trafficlights.log