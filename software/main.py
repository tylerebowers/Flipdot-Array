from interface.display_simulator import Display
#from interface.display import Display
import runners
import uvicorn
import logging
import threading
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates

d = Display()
#runners.self_test(d)

identities = {
    "Clock": runners.Clock,
    "Game of Life": runners.GameOfLife,
    "Off": runners.Off
}
new_mode = {"mode":"Clock", "params":{}}  

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
                    logging.ERROR("Mode not in identities")
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
            return templates.TemplateResponse("index.html", {"request": request, "display_mode": new_mode.get("mode", None)})
        
        
    def run(self):
        uvicorn.run(self.app, host="0.0.0.0", port=8000)
    

if __name__ == "__main__":
    server = WebServer()
    runner = Runner()
    threading.Thread(target=server.run).start()
    runner.run()
