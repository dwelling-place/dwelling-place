"""
Quick run a development server
"""
import red
import red.settings
from werkzeug.serving import run_simple

config = red.settings.get_config('dev')
app = red.create_app(config)
app.debug = True

run_simple('localhost', 5000, app,
           use_reloader=True, use_debugger=True, use_evalex=True)
