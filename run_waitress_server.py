import sys, os  
from waitress import serve  
sys.path.insert(0, './app')
from app import app
HOST = os.environ.get('SERVER_HOST', 'localhost')
PORT = int(os.environ.get('SERVER_PORT'))
serve(app, host=HOST, port=PORT)