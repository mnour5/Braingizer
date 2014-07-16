UI_Path=Resources/UI

clear

echo -e "\e[1;37mGenerating UIs..."
echo -e "\e[1;31m   Generating MainUI"
pyuic4 -o $UI_Path/MainUI/gui_main.py $UI_Path/MainUI/gui_main.ui

echo -e "\e[1;31m   Generating SensorsUI"
pyuic4 -o $UI_Path/SensorsUI/gui_sensors.py $UI_Path/SensorsUI/gui_sensors.ui

echo -e "\e[1;31m   Generating DetectUI"
pyuic4 -o $UI_Path/DetectUI/gui_detect.py $UI_Path/DetectUI/gui_detect.ui

echo -e "\e[1;37m\nStarting Braingizer-Detector\n\e[0m"
python DetectorGUI.py