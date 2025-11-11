# app.wsgi
# Drop this file in your site's document root (for DirectAdmin: public_html/app.wsgi)
# Replace /home/username/domains/your-domain.com/public_html with your actual path.
import sys
import os

# Add application directory to path
sys.path.insert(0, '/home/username/domains/your-domain.com/public_html')

# Activate virtual environment (optional but recommended)
activate_this = '/home/username/domains/your-domain.com/public_html/venv/bin/activate_this.py'
if os.path.exists(activate_this):
    with open(activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))

# Import the Flask application
from app import app as application
