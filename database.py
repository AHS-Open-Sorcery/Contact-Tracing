import json
from event import Event
from typing import Optional
from datetime import date

with open('events.json', 'w+') as f:
    x = f.read()
    if x == '': x = '[]'
    db = json.loads(x)


def store_event(evt: Event):
    newitem = {
        'type': 'event',
        'id': evt.id,
        'name': evt.name,
        'creator': evt.creator_email,
        'date': evt.date.isoformat(),
        'fips': evt.fips,
        'seats': evt.seats
    }
    stored = False
    for i, item in enumerate(db):
        if item['id'] == evt.id:
            db[i] = newitem
            stored = True
            break
    if not stored: db.append(newitem)
    with open('events.json', 'w') as f:
        json.dump(db, f)


def load_event(_id: str) -> Optional[Event]:
    for item in db:
        if item['id'] == _id:
            return parse_event(item)


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
    return len(db)
