echo RaindropInstaller v1
echo WARNING: Before running this installer, ensure python3 is installed on your system. \nPress ENTER to continue...
read
echo Installing pip dependencies...
curl https://raw.githubusercontent.com/metalfoxdev/Raindrop/main/pip_depends.txt >> pip_depends.txt
pip install # put stuff and depends here
