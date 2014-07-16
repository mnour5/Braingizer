_currentDir="`pwd`"

clear

echo -e "\e[1;31mInstalling PyQt4...\n\e[0m"
sudo apt-get install build-essential python2.7-dev libxext-dev qt4-dev-tools python-sip python-sip-dev python-qt4 python-qt4-dev pyqt4-dev-tools

echo -e "\e[1;31m\nInstalling Octave...\n\e[0m"
sudo apt-get install octave octave-signal octave-statistics octave-geometry

echo -e "\e[1;31m\nInstalling PyUSB, Oct2Py and BeautifulSoup...\n\e[0m"
sudo apt-get install python-pip
sudo pip install pyusb oct2py beautifulsoup4

echo -e "\e[1;31m\nInstalling PyCrypto, NumPy, SciPy and Matplotlib...\n\e[0m"
sudo apt-get install python-pycryptopp python-numpy python-scipy python-matplotlib

echo -e "\e[1;31m\nInstalling python-emotiv...\n\e[0m"
cd ~
wget --output-document=python-emotiv.zip https://github.com/ozancaglayan/python-emotiv/archive/master.zip
unzip python-emotiv.zip
cd python-emotiv-master
sudo python setup.py install

echo -e "\e[1;31m\nDependencies are successfully installed.\n\e[0m"
cd "$_currentDir"