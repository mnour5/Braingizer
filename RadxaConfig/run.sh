UI_Path=Resources/UI

clear

echo -e "\e[1;37mGenerating UIs..."
echo -e "\e[1;31m   Generating MainUI"
pyuic4 -o $UI_Path/MainUI/gui_main.py $UI_Path/MainUI/gui_main.ui

echo -e "\e[1;37m\nStarting Radxa Config\n\e[0m"
python RadxaConfigGUI.py