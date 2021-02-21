import uvicorn
from blacksheep.server import Application
from blacksheep.server.bindings import FromForm
from blacksheep.server.templating import use_templates
from blacksheep.server.responses import redirect
from jinja2 import PackageLoader
from event import Event
import json
import database as db
from datetime import datetime, date
from nanoid import generate

app = Application()
view = use_templates(app, loader=PackageLoader('app', 'templates'))


@app.route('/')
def home():
    return view('index', {})


@app.route('/create-event')
def create_event():
    return view('create-event', {})


@app.route('/event-layout')
def event_layout():
    return view('event-layout', {})


@app.route('/about')
def about():
    return view('about', {})


@app.route('/join-event')
def join_event():
    return view('join-event', {})


class EventCreationInput:
    event_name: str
    event_date: str
    event_location: str
    event_organizer: str
    event_population: int
    event_seats: int

    def __init__(self, event_name: str, event_date: str, event_location: str, event_organizer: str,
                 event_population: int, event_seats: int) -> None:
        self.event_name = event_name
        self.event_date = event_date
        self.event_location = event_location
        self.event_organizer = event_organizer
        self.event_population = event_population
        self.event_seats = event_seats


@app.router.post('/event-creation-endpoint')
async def create_event_from_post(input: FromForm[EventCreationInput]):
    data = input.value

    evt = Event(
        id=generate(size=8),
        name=data.event_name,
        creator_email=data.event_organizer,
        date=datetime.strptime(data.event_date, '%b %d, %Y'),
        fips=int(data.event_location),
        seats=[]
    )
    db.store_event(evt)
    return redirect('/event-layout?id=' + evt.id)


class EventJoinData:
    seat_number: int

    def __init__(self, seat_number: int) -> None:
        self.seat_number = seat_number


@app.router.post('/join-event-endpoint')
async def join_event_from_post(input: FromForm[EventJoinData]):
    data = input.value

    print(data.seat_number)


app.serve_files('static')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=42069)
