sudo apt-get update
sudo apt upgrade
wget https://davesteele.github.io/comitup/deb/davesteele-comitup-apt-source_1.2_all.deb
sudo dpkg -i davesteele-comitup-apt-source*.deb
sudo apt-get update
sudo apt upgrade
sudo apt install comitup
sudo systemctl enable NetworkManager.service
wget https://github.com/tylerebowers/Flipdot-Array/archive/refs/heads/main.zip
unzip main.zip
cd Flipdot-Array-main/software/
sudo apt install python3-numpy
