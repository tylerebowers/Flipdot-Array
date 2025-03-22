sudo apt update
sudo apt upgrade -y
wget https://davesteele.github.io/comitup/deb/davesteele-comitup-apt-source_1.2_all.deb
sudo dpkg -i davesteele-comitup-apt-source*.deb
sudo apt update
sudo apt upgrade -y
sudo apt install comitup -y
sudo systemctl enable NetworkManager.service
wget -O main.zip https://github.com/tylerebowers/Flipdot-Array/archive/refs/heads/main.zip
unzip main.zip
cd Flipdot-Array-main/software/
echo "source ~/.global_venv/bin/activate" >> .bashrc
sudo apt install screen python3-numpy python3-uvicorn python3-fastapi python3-requests -y

#edit with sudo nano /etc/systemd/system/flipdots.service
SERVICE_FILE="/etc/systemd/system/flipdots.service"

sudo tee $SERVICE_FILE > /dev/null <<EOL
[Unit]
Description=Startup flipdots controller script service
After=network.target

[Service]
User=$USER
WorkingDirectory=/home/$USER/Flipdot-Array-main/software/
ExecStart=/usr/bin/screen -S flipdots-service -dm /usr/bin/python3 main.py
Restart=always
Type=forking

[Install]
WantedBy=multi-user.target
EOL

sudo systemctl daemon-reload
sudo systemctl enable flipdots.service
echo "Done, rebooting"
sudo reboot now

