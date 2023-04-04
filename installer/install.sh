clear
echo RaindropInstaller v1
echo WARNING: Before running this installer, ensure python3 and pip are installed on your system. \ Press ENTER to continue...
read
echo Installing pip dependencies...
pip3 install requests pyfiglet termcolor
clear
usrname=$(whoami)
cd /home/$usrname/.local/share
mkdir RaindropWeather
cd RaindropWeather
