from blacksheep.server import Application
from blacksheep.server.templating import use_templates
from jinja2 import PackageLoader

app = Application()
view = use_templates(app, loader=PackageLoader('server', 'templates'))

@app.route('/')
def home():
    return view('home', {'example': 'yes'})