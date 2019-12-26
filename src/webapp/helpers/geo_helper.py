import math

from dataclasses import dataclass

@dataclass
class Point:
    lat: float
    lon: float

def distance(point1: Point, point2: Point):
    lon1, lat1, lon2, lat2 = map(
        math.radians, [point1.lon, point1.lat, point2.lon, point2.lat]
        )
    return 6371 * (
        math.acos(
            math.sin(lat1) * math.sin(lat2)
            + math.cos(lat1) * math.cos(lat2) * math.cos(lon1 - lon2),
        )
    )