#!/usr/bin/env python3
"""
Quick diagnostic script to test Flask app routing
Run this to verify the install route exists
"""

import sys
import os

# Add application directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app import app
    
    print("=" * 60)
    print("CANNASPOT ROUTE DIAGNOSTICS")
    print("=" * 60)
    
    # List all routes
    print("\n📋 Registered Routes:")
    print("-" * 60)
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'})),
            'path': str(rule)
        })
    
    # Sort by path
    routes.sort(key=lambda x: x['path'])
    
    # Check if install route exists
    install_exists = any(r['path'] == '/install' for r in routes)
    
    for route in routes:
        if '/install' in route['path']:
            print(f"✅ {route['path']:30} [{route['methods']:15}] -> {route['endpoint']}")
        else:
            print(f"   {route['path']:30} [{route['methods']:15}] -> {route['endpoint']}")
    
    print("-" * 60)
    print(f"Total routes: {len(routes)}")
    
    if install_exists:
        print("\n✅ /install route IS registered!")
    else:
        print("\n❌ /install route NOT found!")
    
    print("\n🔧 App Configuration:")
    print(f"   DEBUG: {app.config.get('DEBUG', False)}")
    print(f"   SECRET_KEY: {'Set' if app.config.get('SECRET_KEY') else 'Missing'}")
    print(f"   DATABASE: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')[:50]}...")
    
    print("\n✅ Flask app loaded successfully!")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ ERROR loading Flask app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
