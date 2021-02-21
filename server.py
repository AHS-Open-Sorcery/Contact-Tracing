import uvicorn
from blacksheep.server import Application
from blacksheep.server.bindings import FromForm
from blacksheep.server.bindings import Request
from blacksheep.server.templating import use_templates
from blacksheep.server.responses import redirect, status_code, text, json as res_json
from jinja2 import PackageLoader
from event import Event
from fips import get_fips
import json
from event_risk import event_risk
import database as db
from datetime import datetime, date
from nanoid import generate

app = Application()
get = app.router.get
post = app.router.post
view = use_templates(app, loader=PackageLoader('app', 'templates'))


@app.route('/')
def home():
    return view('index', {})


@app.route('/create-event')
def create_event():
    return view('create-event', {})


@get('/event-layout')
def event_layout(id: str, seats: int):
    evt = db.load_event(id)
    if evt is None:
        return status_code(422, f'unknown event with id {id}')

    risk = event_risk(evt, seats)
    return view('event-layout', {'id': id, 'seats': seats, 'risk': risk, 'name': evt.name})


@post('/event-layout')
async def post_event_layout(request: Request):
    form = await request.json()
    print(form)
    evt = db.load_event(form['id'])
    if evt is None:
        return status_code(422, f'unknown event with id {id}')

    evt.seats = form['layout']['seats']
    db.store_event(evt)
    return status_code(200, 'success')


@get('/event-created')
def event_created(id: str):
    evt = db.load_event(id)
    if evt is None:
        return status_code(422, f'unknown event with id {id}')

    return view('event-created', {'event': evt})


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
    fips = get_fips(data.event_location)
    print(f'fips = {fips}')

    evt = Event(
        id=generate(size=8),
        name=data.event_name,
        creator_email=data.event_organizer,
        date=datetime.strptime(data.event_date, '%b %d, %Y').date(),
        fips=int(fips),
        seats=[]
    )
    db.store_event(evt)
    return redirect(f'/event-layout?id={evt.id}&seats={data.event_seats}')


class EventJoinData:
    seat_number: int

    def __init__(self, seat_number: int) -> None:
        self.seat_number = seat_number


@get('/join-event/{event_id}')
async def join_event_from_post(request: Request):
    event_id = request.route_values['event_id']
    evt = db.load_event(event_id)
    if evt is None:
        return status_code(422, f'unknown event id: {event_id}')

    print(evt.seats)
    return view('join-event', {'event': evt, 'risk': event_risk(evt, len(evt.seats))})


@post('/join-event-endpoint')
async def join_event_post(request: Request):
    js = await request.json()
    seat = js['seat_number']
    _id = js['id']
    evt = db.load_event(_id)
    for i, s_o in enumerate(evt.seats):
        if s_o['number'] == seat:
            evt.seats[i]['occupied'] = True
    db.store_event(evt)
    return status_code(200, 'success')


@get('/event-joined')
def event_joined(id: str):
    evt = db.load_event(id)
    return view('event-joined', {'event': evt, 'risk': event_risk(evt, len(evt.seats))})


app.serve_files('static')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=42069)
