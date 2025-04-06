# do this after the setup_rpi.sh script is run
sudo nano /boot/firmware/cmdline.txt
# add maxcpus=1 after console=tty1, reboot, check with lscpu

# To allow shutdowns and reboots from the web GUI password auth must be removed.
# edit the sudoers file: sudo visudo
# and add the following line:
admin ALL=(ALL) NOPASSWD: /bin/systemctl poweroff, /bin/systemctl reboot, /bin/systemctl stop flipdots.service, /bin/systemctl start flipdots.service, /bin/systemctl restart flipdots.service
