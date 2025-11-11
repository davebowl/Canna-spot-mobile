#!/bin/bash
# Gunicorn startup script for LiteSpeed/DirectAdmin
# Make executable: chmod +x start_gunicorn.sh

# Change this to your actual path
APP_DIR="/home/username/domains/your-domain.com/public_html"

cd "$APP_DIR"

# Activate virtual environment
source venv/bin/activate

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Start Gunicorn
# -w 4: 4 worker processes
# -b 127.0.0.1:8000: Bind to localhost port 8000
# --timeout 300: 5 minute timeout for large uploads
# --access-logfile: Log requests
# --error-logfile: Log errors
# --daemon: Run in background

gunicorn -w 4 \
  -b 127.0.0.1:8000 \
  --timeout 300 \
  --access-logfile access.log \
  --error-logfile error.log \
  --daemon \
  app:app

echo "Gunicorn started on port 8000"
