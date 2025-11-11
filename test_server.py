#!/usr/bin/env python3
"""
Simple test to verify the server can run Python and import Flask
Upload this to your server and access it via browser
"""
print("Content-Type: text/html\n")
print("<html><body>")
print("<h1>CannaSpot Server Test</h1>")

import sys
print(f"<p>✅ Python Version: {sys.version}</p>")
print(f"<p>✅ Python Path: {sys.executable}</p>")

try:
    import flask
    print(f"<p>✅ Flask Installed: {flask.__version__}</p>")
except ImportError as e:
    print(f"<p>❌ Flask NOT installed: {e}</p>")

try:
    from app import app
    print(f"<p>✅ App module loaded successfully</p>")
    print(f"<p>✅ Routes registered: {len(list(app.url_map.iter_rules()))}</p>")
    
    # Check if /install exists
    install_route = any(str(rule) == '/install' for rule in app.url_map.iter_rules())
    if install_route:
        print(f"<p>✅ /install route EXISTS</p>")
    else:
        print(f"<p>❌ /install route NOT FOUND</p>")
        
except Exception as e:
    print(f"<p>❌ Error loading app: {e}</p>")
    import traceback
    print(f"<pre>{traceback.format_exc()}</pre>")

print("</body></html>")
