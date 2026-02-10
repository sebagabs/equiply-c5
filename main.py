import math

from fastapi import FastAPI
from pydantic import BaseModel


class VelocityRequest(BaseModel):
    coordinates: list[dict[str, float]]

app = FastAPI()

@app.post("/calculate-velocity")
def calculate_velocity(item: VelocityRequest):
    return calculate_helper(item.coordinates)


def calculate_helper(coordinates: list[dict[str, float]]) -> dict:
    return {
        "distance": distance(coordinates),
        "speed": speed(coordinates),
        "velocity": velocity(coordinates),
    }


def distance(coordinates: list[dict[str, float]]) -> float:
    p1 = (coordinates[0].get('x', 0), coordinates[0].get('y', 0), coordinates[0].get('z', 0))
    p2 = (coordinates[1].get('x', 0), coordinates[1].get('y', 0), coordinates[1].get('z', 0))
    p3 = (coordinates[2].get('x', 0), coordinates[2].get('y', 0), coordinates[2].get('z', 0))
    return round(math.dist(p1, p2) + math.dist(p2, p3), 2)


def speed(coordinates: list[dict[str, float]]) -> float:
    dist = distance(coordinates)
    time_elapsed = coordinates[2].get('timestamp', 1) - coordinates[0].get('timestamp', 0)
    return round(dist / time_elapsed, 2) if time_elapsed > 0 else 0


def velocity(coordinates: list[dict[str, float]]) -> dict[str, float]:
    time_elapsed = coordinates[2].get('timestamp', 1) - coordinates[0].get('timestamp', 0)
    return {
        'x': round((coordinates[2].get('x', 0) - coordinates[0].get('x', 0)) / time_elapsed, 2) if time_elapsed > 0 else 0,
        'y': round((coordinates[2].get('y', 0) - coordinates[0].get('y', 0)) / time_elapsed, 2) if time_elapsed > 0 else 0,
        'z': round((coordinates[2].get('z', 0) - coordinates[0].get('z', 0)) / time_elapsed, 2) if time_elapsed > 0 else 0,
    }
