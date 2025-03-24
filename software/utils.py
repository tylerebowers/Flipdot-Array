import time

def self_test(d):
    d.all_on()
    time.sleep(2)
    d.all_off()
    time.sleep(2)

def set_settings(d, new_settings):
    d.delay = max(int(new_settings.get("delay", 10) or 10),0)
    d.horizontal = "WE" if new_settings.get("horizontal", "WE") == "WE" else "EW"
    d.vertical = "NS" if new_settings.get("vertical", "NS") == "NS" else "SN"
    d.order = "XY" if new_settings.get("order", "XY") == "XY" else "YX"