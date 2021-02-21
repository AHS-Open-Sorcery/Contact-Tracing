from tinydb import TinyDB, Query
from event import Event
from typing import Optional
from datetime import date

db = TinyDB('events.json')


def store_event(evt: Event) -> int:
    return db.insert({
        'type': 'event',
        'id': evt.id,
        'name': evt.name,
        'creator': evt.creator_email,
        'date': evt.date.isoformat(),
        'fips': evt.fips,
        'seats': evt.seats
    })


def load_event(_id: int) -> Optional[Event]:
    Event = Query()
    jsons = db.search(Event.id == _id)
    if len(jsons) == 0:
        return None

    return parse_event(jsons[0])


def parse_event(obj: dict) -> Event:
    return Event(
        id=obj['id'],
        name=obj['name'],
        creator_email=obj['creator'],
        date=date.fromisoformat(obj['date']),
        fips=obj['fips'],
        seats=obj['seats']
    )


def num_events() -> int:
    return len(db.all())
