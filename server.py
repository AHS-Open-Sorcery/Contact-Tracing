import uvicorn
from blacksheep.server import Application
from blacksheep.server.bindings import FromForm
from blacksheep.server.templating import use_templates
from jinja2 import PackageLoader

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



app.serve_files('static')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=42069)
