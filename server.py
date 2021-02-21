from blacksheep.server import Application
from blacksheep.server.templating import use_templates
from jinja2 import PackageLoader
import uvicorn

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


app.serve_files('static')


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=42069)