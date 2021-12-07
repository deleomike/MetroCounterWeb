from typing import Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from MemoryManager import MemoryManager

class LocationPayload(BaseModel):
    location: str
    num_data_points: int
    # timestamps: list
    data: list


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = MemoryManager()


@app.post("/crowd_data", status_code=200)
async def receive_data(payload: LocationPayload):
    location = payload.location

    for datapoint in payload.data:
        manager.insert_data(location=location, data_point=datapoint)

    manager.fit_regression(location=location)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/crowd_data/{location}/current")
async def read_current_value(location: str):
    try:
        val = manager.get_current(location)
    except KeyError as e:
        return JSONResponse({"Error": f"Location {location} not valid, does not exist"}, status_code=400)
    return {"location": location, "value": val}


@app.get("/crowd_data/{location}/prediction")
async def make_prediction(location: str):
    try:
        predictions = manager.get_prediction(location)
    except KeyError as e:
        return JSONResponse({"Error": f"Location {location} not valid, does not exist"}, status_code=400)
    return {"location": location, "value": predictions}

@app.get("/crowd_data/{location}/hour")
async def read_hour_data(location: str):
    try:
        val = manager.get_hour(location)
    except KeyError as e:
        return JSONResponse({"Error": f"Location {location} not valid, does not exist"}, status_code=400)
    return {"location": location, "value": val}


@app.get("/crowd_data/{location}/day")
async def read_day_data(location: str):
    try:
        val = manager.get_day(location)
    except KeyError as e:
        return JSONResponse({"Error": f"Location {location} not valid, does not exist"}, status_code=400)
    return {"location": location, "value": val}


@app.get("/crowd_data/{location}/week")
async def read_week_data(location: str):
    try:
        val = manager.get_week(location)
    except KeyError as e:
        return JSONResponse({"Error": f"Location {location} not valid, does not exist"}, status_code=400)
    return {"location": location, "value": val}


@app.get("/crowd_data/{location}/month")
async def read_month_data(location: str):
    try:
        val = manager.get_month(location)
    except KeyError as e:
        return JSONResponse({"Error": f"Location {location} not valid, does not exist"}, status_code=400)
    return {"location": location, "value": val}