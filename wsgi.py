##  /var/www/jibbius_pythonanywhere_com_wsgi.py
import sys

# Add project directory to the sys.path , before further imports
project_home = '/home/jibbius/flask-tic-tac-toe'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Import from the project directory
from webapp import create_app
from config import DevConfig
config = DevConfig()

# Create flask app, but need to call it "application" for WSGI to work
application = create_app(config)