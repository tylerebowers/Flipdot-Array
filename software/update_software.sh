# This script updates to the latest flipdot software.

echo "Stopping service"
sudo systemctl stop flipdots.service
echo "Updating software"
git fetch --all
git reset --hard origin/main
echo "Starting service"
sudo systemctl start flipdots.service