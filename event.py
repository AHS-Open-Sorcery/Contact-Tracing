from dataclasses import dataclass
from datetime import date
from typing import List, Dict


@dataclass
class Event:
    id: str
    name: str
    creator_email: str
    date: date
    fips: int
    seats: List[Dict]
