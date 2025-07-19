/*
READ FIRST
It is not recommended to change this file if you do not know what you are doing.
Doing so can cause PERMANENT DAMAGE to the display or the RPi (if done incorrectly).
Edit at your own risk.

This is a C++ based interface for the display.

After changes recompile (on the rpi) with:
c++ -O3 -Wall -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) display.cpp -o display$(python3-config --extension-suffix) -lwiringPi
*/

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <wiringPi.h>
#include <signal.h>
#include <unistd.h>
#include <vector>
#include <iostream>
#include <thread>

using namespace std;

class Display {
private:
    const int _ser = 18;
    const int _oe = 23;
    const int _rclk = 24;
    const int _srclk = 25;
    const int _srclr = 8;
    vector<uint32_t> shown = vector<uint32_t>(21, 0); 

public:
    uint32_t delay = 10000;
    string horizontal = "WE";
    string vertical = "NS";
    string order = "XY";

    Display() {
        wiringPiSetupGpio();  

        pinMode(_ser, OUTPUT);
        pinMode(_oe, OUTPUT);
        pinMode(_rclk, OUTPUT);
        pinMode(_srclk, OUTPUT);
        pinMode(_srclr, OUTPUT);

        all_off(true);
        _disable();
        _clear();
    }

    ~Display() {
        _disable();
        _clear();
    }

    vector<uint32_t> get_shown() {
        // Get shown
        return shown;
    }

    bool check_shown(int x, int y) {
        // Check if dot is shown at x, y
        if (!(x >= 0 && x < 21 && y >= 0 && y < 7)){
            return false;
        } else {
            return shown[x] & (1ULL << y);
        }
    }

    void _disable() {
        // Disable display
        digitalWrite(_oe, HIGH);
    }

    void _enable() {
        // Enable display
        digitalWrite(_oe, LOW);
    }

    void _clear() {
        // Clear registers
        digitalWrite(_srclr, LOW);
        digitalWrite(_srclr, HIGH);
        digitalWrite(_ser, LOW);
    }

    void write_dot(int x, int y, bool state, bool force = false) {
        // Write dot at x, y with state and don't check shown if force
        _disable();
        _clear();
        if (!(x >= 0 && x < 21 && y >= 0 && y < 7)) return;

        unsigned long long serial_data = 0;

        if (state && (!(shown[x] & (1ULL << y)) || force)) {
            serial_data |= (1ULL << y);  // Set row
            serial_data |= (1ULL << (x + 24 + (8 * (x / 8))));  // Set col
            shown[x] |= (1ULL << y);
        } 
        else if (!state && ((shown[x] & (1ULL << y)) || force)) {
            serial_data |= (1ULL << (y + 8));  // Set row
            serial_data |= (1ULL << (x + 16 + (8 * (x / 8))));  // Set col
            shown[x] &= ~(1ULL << y);
        }

        if (serial_data > 0) {
            //printf("%d %d %d %llu\n", x, y, state, serial_data);
            for (int i = 63; i >= 0; i--) {
                digitalWrite(_ser, (serial_data & (1ULL << i)) ? HIGH : LOW);
                digitalWrite(_srclk, HIGH);
                digitalWrite(_srclk, LOW);
            }

            // Move data into registers
            digitalWrite(_rclk, HIGH);
            digitalWrite(_rclk, LOW);
            digitalWrite(_ser, LOW);

            _enable();
            this_thread::sleep_for(chrono::microseconds(150));
            _disable();
        }
    }

    void all_off(bool force = false) {
        // turn all dots off
        for (int y = 0; y < 7; y++) {
            for (int x = 0; x < 21; x++) {
                write_dot(x, y, false, force);
                this_thread::sleep_for(chrono::microseconds(delay));
            }
        }
        _disable();
        _clear();
    }

    void all_on(bool force = false) {
        // turn all dots on
        for (int y = 0; y < 7; y++) {
            for (int x = 0; x < 21; x++) {
                write_dot(x, y, true, force);
                this_thread::sleep_for(chrono::microseconds(delay));
            }
        }
        _disable();
        _clear();
    }


    void write_display(vector<int> new_display, int start_x = 0, int start_y = 0, bool force = false) {
        // Write display bitwise array starting from start_x, start_y and don't check shown if force
        vector<int> x_range;
        if (horizontal == "WE") { // West to East
            for (int i = start_x; i < min(21, (int)new_display.size() + start_x); i++) {
                x_range.push_back(i);
            }
        } else { // East to West
            for (int i = min(20, (int)new_display.size() + start_x-1); i >= start_x; i--) {
                x_range.push_back(i);
            }
        }

        vector<int> y_range;
        if (vertical == "NS") { // North to South
            for (int i = start_y; i < 7; i++) {
                y_range.push_back(i);
            }
        } else { // South to North
            for (int i = 7; i >= start_y; i--) {
                y_range.push_back(i);
            }
        }

        if (order == "XY") {
            for (int x : x_range) {
                for (int y : y_range) {
                    this_thread::sleep_for(chrono::microseconds(delay));
                    write_dot(x, y, new_display[x - start_x] & (1ULL << y), force);
                }
            }
        } else if (order == "YX") {
            for (int y : y_range) {
                for (int x : x_range) {
                    this_thread::sleep_for(chrono::microseconds(delay));
                    write_dot(x, y, new_display[x - start_x] & (1ULL << y), force);
                }
            }
        }
        _disable();
        _clear();
    }

};


PYBIND11_MODULE(display, m) {
    pybind11::class_<Display>(m, "Display")
    .def(pybind11::init<>())  // Bind constructor
    .def_readwrite("delay", &Display::delay)
    .def_readwrite("horizontal", &Display::horizontal)
    .def_readwrite("vertical", &Display::vertical)
    .def_readwrite("order", &Display::order)
    .def("write_dot", [](Display &self, 
                         int x, 
                         int y, 
                         bool state, 
                         bool force = false) {
        try {
            self.write_dot(x, y, state, force);
        } catch (...) {
            self._disable();
            self._clear();
            throw;
        }
    },
        pybind11::arg("x"),
        pybind11::arg("y"),
        pybind11::arg("state"),
        pybind11::arg("force") = false)
    .def("get_shown", &Display::get_shown)
    .def("check_shown", &Display::check_shown, 
        pybind11::arg("x"),
        pybind11::arg("y"))
    .def("all_on", &Display::all_on, 
        pybind11::arg("force") = false)  
    .def("all_off", &Display::all_off, 
        pybind11::arg("force") = false)
    .def("write_display", [](Display &self, 
                             vector<int> new_display, 
                             int start_x = 0, 
                             int start_y = 0, 
                             bool force = false) {
        try {
            self.write_display(new_display, start_x, start_y, force);
        } catch (...) {
            self._disable();
            self._clear();
            throw;
        }
    }, 
        pybind11::arg("new_display"),
        pybind11::arg("start_x") = 0,
        pybind11::arg("start_y") = 0,
        pybind11::arg("force") = false);
}

/*
after changes recompile with:
c++ -O3 -Wall -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) display.cpp -o display$(python3-config --extension-suffix) -lwiringPi
*/
