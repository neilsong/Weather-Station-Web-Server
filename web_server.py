# with code from https://github.com/roniemartinez/real-time-charts-with-fastapi

import asyncio
import json
import logging
import sys
from datetime import datetime
from typing import Iterator

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from collections import OrderedDict

app = FastAPI()

c_test = OrderedDict()

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)
application = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def display():
    return "alive"

async def generator(request: Request) -> Iterator[str]:
    """
    Generates random value between 0 and 100
    :return: String containing current timestamp (YYYY-mm-dd HH:MM:SS) and randomly generated data.
    """
    global c_test
    client_ip = request.client.host

    logger.info("Client %s connected", client_ip)

    while True:
        json_data = json.dumps(
            {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "value": c_test
            }
        )
        yield f"data:{json_data}\n\n"
        await asyncio.sleep(0.5)

@app.get("/display", response_class=HTMLResponse)
async def index(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/test-data")
async def chart_data(request: Request) -> StreamingResponse:
    response = StreamingResponse(generator(request), media_type="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

# query url parameters
@app.api_route("/update", methods=["GET"])
async def update(wind_speed: float, wind_direction: float, temp:float, humidity: float, id: str):
    global c_test
    c_test.update({
        id: {
            'wind_speed': wind_speed,
            'wind_direction': wind_direction,
            'temp': temp,
            'humidity': humidity
        }
    })
    
    # send update to mongodb database

    return "done updating"

import nest_asyncio
import uvicorn
nest_asyncio.apply()

from pyngrok import ngrok, conf
pyngrok_config = conf.PyngrokConfig()
pyngrok_config.auth_token = "1rKW512YaaAic3Lmwx2ZKtyfs1i_79mpcmRvUwQEVb4GTAeCP"
ngrok.connect(8000, subdomain="weatherstation", pyngrok_config=pyngrok_config)

uvicorn.run(app, port=8000)
