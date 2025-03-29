# This script updates to the latest flipdot software.

echo "Stopping service"
sudo systemctl stop flipdots.service
echo "Updating software"
git fetch --all
git reset --hard origin/main

read -t 10 -r -p "Recompile interface? [y/N] (continuing in 10s) " response 
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
    cd interface
    c++ -O3 -Wall -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) display.cpp -o display$(python3-config --extension-suffix) -lwiringPi
    cd ..
fi

echo "Starting service"
sudo systemctl start flipdots.service