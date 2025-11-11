#!/bin/bash
# Pre-deployment check script

echo "🔍 CannaSpot v3.6 Deployment Readiness Check"
echo "=============================================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
python3 --version
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "✓ Virtual environment found"
else
    echo "⚠️  Virtual environment not found - run: python3 -m venv venv"
fi
echo ""

# Check required files
echo "✓ Checking required files..."
required_files=("app.py" "models.py" "requirements.txt" "migrate_db.py")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file MISSING!"
    fi
done
echo ""

# Check directories
echo "✓ Checking upload directories..."
required_dirs=("uploads" "uploads/videos" "uploads/thumbnails" "uploads/avatars" "uploads/ads" "static" "templates")
for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✓ $dir"
    else
        echo "  ⚠️  $dir missing - will be created"
        mkdir -p "$dir"
    fi
done
echo ""

# Check database
if [ -f "cannaspot.db" ]; then
    echo "✓ Database file exists"
    echo "  Run migration: python migrate_db.py"
else
    echo "⚠️  Database not initialized"
    echo "  Will be created on first /install visit"
fi
echo ""

# Check environment variables
echo "✓ Checking environment configuration..."
if [ -z "$SECRET_KEY" ]; then
    echo "  ⚠️  SECRET_KEY not set (will use default - CHANGE FOR PRODUCTION!)"
else
    echo "  ✓ SECRET_KEY configured"
fi

if [ -z "$DATABASE_URL" ]; then
    echo "  ℹ️  DATABASE_URL not set (will use SQLite)"
else
    echo "  ✓ DATABASE_URL configured"
fi

if [ "$FLASK_ENV" = "production" ]; then
    echo "  ✓ FLASK_ENV=production"
else
    echo "  ⚠️  FLASK_ENV not set to production (debug mode enabled)"
fi
echo ""

echo "=============================================="
echo "📝 Next Steps:"
echo "1. Set environment variables (SECRET_KEY, FLASK_ENV=production)"
echo "2. Install dependencies: pip install -r requirements.txt"
echo "3. Run migration: python migrate_db.py"
echo "4. Set permissions: chmod -R 777 uploads/"
echo "5. Visit /install to create admin account"
echo "6. Deploy with gunicorn or configure Apache/Nginx"
echo ""
echo "✅ Ready for deployment!"
