clear
echo RaindropInstaller for v1.0
echo WARNING: Before running this installer, ensure python3 and pip are installed on your system. \ Press ENTER to continue...
read
echo Installing pip dependencies...
pip3 install requests pyfiglet termcolor
clear
echo Getting username
usrname=$(whoami)
echo finding home directory
cd /home/$usrname/.local/share
echo making raindrop app folder
mkdir RaindropWeather
echo entering raindrop app folder
cd RaindropWeather
echo getting logo
curl -O icon.png "https://raw.githubusercontent.com/metalfoxdev/Raindrop/main/assets/logo.png"
# clear
echo writing desktop file
echo "[Desktop Entry]" >> raindrop.desktop
echo "Version=1.0" >> raindrop.desktop
echo "Name=Raindrop" >> raindrop.desktop
echo "Comment=A slick and intuitive weather app for the Linux terminal" >> raindrop.desktop
echo "Exec=python3 main.py" >> raindrop.desktop
echo "Icon=/home/$usrname/.local/share/RaindropWeather/icon.png" >> raindrop.desktop
echo "Path=/home/$usrname/.local/share/RaindropWeather" >> raindrop.desktop
echo "Terminal=true" >> raindrop.desktop
echo "Type=Application" >> raindrop.desktop
echo "Categories=Utility;Application;" >> raindrop.desktop
