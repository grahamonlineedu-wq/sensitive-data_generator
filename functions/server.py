import sys
import os

# Add project root to path so it can import server.py and wsgi.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from wsgi import handler as server_handler

def handler(event, context):
    return server_handler(event, context)
