UI_Path=Resources/UI

clear

echo -e "\e[1;37mGenerating UIs..."
echo -e "\e[1;31m   Generating MainUI"
pyuic4 -o $UI_Path/MainUI/gui_main.py $UI_Path/MainUI/gui_main.ui

echo -e "\e[1;31m   Generating SensorsUI"
pyuic4 -o $UI_Path/SensorsUI/gui_sensors.py $UI_Path/SensorsUI/gui_sensors.ui

echo -e "\e[1;31m   Generating TrainUI"
pyuic4 -o $UI_Path/TrainUI/gui_train.py $UI_Path/TrainUI/gui_train.ui

echo -e "\e[1;37m\nStarting Braingizer-Trainer\n\e[0m"
python TrainerGUI.py