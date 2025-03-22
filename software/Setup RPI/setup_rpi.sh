sudo apt update
sudo apt upgrade -y
wget https://davesteele.github.io/comitup/deb/davesteele-comitup-apt-source_1.2_all.deb
sudo dpkg -i davesteele-comitup-apt-source*.deb
sudo apt update
sudo apt upgrade -y
sudo apt install comitup -y
sudo systemctl enable NetworkManager.service
wget https://github.com/tylerebowers/Flipdot-Array/archive/refs/heads/main.zip
unzip main.zip
cd Flipdot-Array-main/software/
sudo apt install screen python3-numpy python3-uvicorn python3-fastapi python3-requests -y
