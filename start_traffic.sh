cd ~/Documents/IoT-proj-trafficlights

source venv/bin/activate

while ! ping -c 1 google.com &>/dev/null; do
	sleep 5
done

echo "Internet connected."

# python ~/Documents/IoT-proj-trafficlights/thread_smart_lights.py
python ~/Documents/IoT-proj-trafficlights/V1/smart_controller_ext_cam_2.py
