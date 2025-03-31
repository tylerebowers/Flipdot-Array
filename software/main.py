import runners
import uvicorn
import threading
import socket
import time
import utils
import os
import platform
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates

if "rpi" in platform.release():
    from interface.display import Display
    PORT = 80
else:
    from interface.display_simulator import Display
    PORT = 8000

class Runner:
    def __init__(self):
        self.runner = None

    def run(self):
        global new_mode
        while True:
            if new_mode != None:
                if new_mode.get("mode", None) in identities.keys():
                    try: 
                        self.runner = identities[new_mode["mode"]](d, new_mode.get("params",{}))
                    except Exception as e:
                        print(e)
                else: 
                    print("Mode not in identities")
                new_mode = None
            else:
                self.runner.update()

class WebServer:
    def __init__(self):
        self.app = FastAPI()
        templates = Jinja2Templates(directory=".")

        @self.app.get("/", response_class=HTMLResponse)
        async def get_index(request: Request):
            global new_mode
            return templates.TemplateResponse("index.html", {"request": request, "display_mode": str(new_mode)})

        @self.app.post("/mode", response_class=HTMLResponse)
        async def set_mode(request: Request):
            global new_mode
            new_mode = await request.json()
            print("Received: ", new_mode)
            #return templates.TemplateResponse("index.html", {"request": request, "display_mode": new_mode.get("mode", None)})
        
        @self.app.post("/settings", response_class=HTMLResponse)
        async def set_settings(request: Request):
            r = await request.json()
            print("Received:", r)
            utils.set_settings(d, r)

        
    def run(self):
        uvicorn.run(self.app, host=ip, port=PORT)

if __name__ == "__main__":
    identities = {
        "Clock": runners.Clock,
        "Game of Life": runners.GameOfLife,
        "Off": runners.Off,
        "Scrolling Text": runners.ScrollingText,
        "Date": runners.Date,
        "Weather": runners.Weather,
        "System": runners.System,
    }
    new_mode = {"mode":"Clock", "params":{}}  
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    # If the script crashes here it will be restarted by systemd

    d = Display()
    utils.self_test(d)
    ip_runner = runners.ScrollingText(d, {"text": ip[[i for i, n in enumerate(ip) if n == '.'][1]:]})
    ip_runner.update()
    del ip_runner
    time.sleep(2)

    server = WebServer()
    runner = Runner()
    threading.Thread(target=server.run).start()
    runner.run()
