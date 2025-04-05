import runners
import uvicorn
import threading
import socket
import time
import utils
import os
import asyncio
import platform
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
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
        self.websocket_client = None
        templates = Jinja2Templates(directory=".")

        @self.app.get("/", response_class=HTMLResponse)
        async def get_index(request: Request):
            global new_mode
            return templates.TemplateResponse("index.html", {"request": request})
        
        @self.app.get("/canvas", response_class=HTMLResponse)
        async def get_index(request: Request):
            global new_mode
            return templates.TemplateResponse("canvas.html", {"request": request})

        @self.app.post("/mode")
        async def set_mode(request: Request):
            if self.websocket_client is None:
                global new_mode
                new_mode = await request.json()
            print("Received: ", new_mode)
            return 

        @self.app.post("/settings")
        async def set_settings(request: Request):
            r = await request.json()
            print("Received:", r)
            d.delay = max(int(r.get("delay", 10) or 10),0)
            d.horizontal = "WE" if r.get("horizontal", "WE") == "WE" else "EW"
            d.vertical = "NS" if r.get("vertical", "NS") == "NS" else "SN"
            d.order = "XY" if r.get("order", "XY") == "XY" else "YX"
            return
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket): 
            if self.websocket_client is not None:
                await self.websocket_client.close(code=1000)  
            await websocket.accept()
            self.websocket_client = websocket
            print("WebSocket client connected")

            global new_mode
            new_mode = {"mode": "Static", "params": {"frame": []}}

            try:
                while True:
                    data = await asyncio.wait_for(websocket.receive_json(), timeout=60) # expects: {"dot":[x,y,state]} or {"frame": [_,_, etc.]}
                    try:
                        if data.get("dot", None) != None:
                            d.write_dot(data["dot"][0], data["dot"][1], bool(data["dot"][2]))
                        elif data.get("frame", None) != None:
                            d.write_display(data["frame"])
                    except Exception as e:
                        print(e)
            except asyncio.TimeoutError:
                print("WebSocket client inactive - disconnecting")
                await websocket.close(code=1001) 
            except WebSocketDisconnect:
                print("WebSocket client disconnected")
            except Exception as e:
                print("WebSocket error:", e)
            finally:
                self.websocket_client = None

        
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
        "Static": runners.Static,
    }
    new_mode = {"mode":"Clock", "params":{"start_hour": 7, "stop_hour": 24, "hours_24": False}}  
    
    print("Getting IP")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    # If the script crashes here it will be restarted by systemd

    d = Display()
    print("Self test")
    utils.self_test(d)
    ip_runner = runners.ScrollingText(d, {"text": ip[[i for i, n in enumerate(ip) if n == '.'][1]:]})
    ip_runner.update()
    del ip_runner
    time.sleep(2)

    print("Starting Webserver")
    server = WebServer()
    runner = Runner()
    threading.Thread(target=server.run).start()
    runner.run()
