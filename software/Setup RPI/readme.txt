# do this after the setup_rpi.sh script is run
sudo nano /boot/firmware/cmdline.txt
# add maxcpus=1 after console=tty1, reboot, check with lscpu
