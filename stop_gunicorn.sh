#!/bin/bash
# Stop Gunicorn process

pkill -f gunicorn
echo "Gunicorn stopped"
