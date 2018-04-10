import sys, os  
from waitress import serve  
sys.path.insert(0, './app')
from app import app
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
serve(app,HOST, PORT)  