#!/bin/bash

# This script updates to the latest flipdot software.
echo "Updating software"

INTERFACE="interface/display.cpp"
before=$(stat -c %Y "$INTERFACE")

git fetch --all
git reset --hard origin/main

after=$(stat -c %Y "$INTERFACE")
if [[ "$before" -ne "$after" ]]; then
    echo "display.cpp has been modified. Recompiling interface."
    response="y"
else
    read -t 5 -r -p "Recompile interface? [y/N] (continuing in 5s) " response 
fi

if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "Compiling interface"
    cd interface
    c++ -O3 -Wall -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) display.cpp -o display$(python3-config --extension-suffix) -lwiringPi
    cd ..
    echo "Interface compiled"
fi

echo "Restarting service"
sudo systemctl restart flipdots.service
