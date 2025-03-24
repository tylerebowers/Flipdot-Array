# This script only need to be run once.
sudo apt update
sudo apt upgrade -y
wget https://davesteele.github.io/comitup/deb/davesteele-comitup-apt-source_1.2_all.deb
sudo dpkg -i davesteele-comitup-apt-source*.deb
sudo apt update
sudo apt upgrade -y
sudo apt install comitup -y
sudo systemctl enable NetworkManager.service
sudo apt install screen python3-numpy python3-uvicorn python3-fastapi python3-requests python3-pybind11 wiringpi git -y
wget https://github.com/WiringPi/WiringPi/releases/download/3.14/wiringpi_3.14_armhf.deb
sudo apt install ./wiringpi_3.14_armhf.deb
git clone https://github.com/tylerebowers/Flipdot-Array
cd Flipdot-Array/software/
#git fetch --all
#git reset --hard origin/main

#edit with sudo nano /etc/systemd/system/flipdots.service
SERVICE_FILE="/etc/systemd/system/flipdots.service"

sudo tee $SERVICE_FILE > /dev/null <<EOL
[Unit]
Description=Startup flipdots controller script service
After=network.target

[Service]
User=root ; since we need port 80 to access from flipdots.local
WorkingDirectory=/home/$USER/Flipdot-Array/software/
ExecStart=/usr/bin/screen -S flipdots-service -dm /usr/bin/python3 main.py
Restart=always
Type=forking

[Install]
WantedBy=multi-user.target
EOL

sudo systemctl daemon-reload
sudo systemctl enable flipdots.service
#sudo systemctl restart flipdots.service
#sudo systemctl stop flipdots.service
echo "Done, rebooting"
sudo reboot now

