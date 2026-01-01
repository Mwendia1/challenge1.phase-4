#!/bin/bash

echo "Starting Flask Superheroes API..."
echo "=================================="

# Check if in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Check if requirements are installed
echo "Checking dependencies..."
pip list | grep -q Flask
if [ $? -ne 0 ]; then
    echo "Installing Flask..."
    pip install Flask==2.3.3 Flask-SQLAlchemy==3.0.5
fi

# Check if database exists
if [ ! -f "superheroes.db" ]; then
    echo "Creating database..."
    python -c "
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print('Database created')
"
    
    echo "Seeding database..."
    python seeds.py
fi

# Start the server
echo "Starting server on http://localhost:5555..."
echo "Press Ctrl+C to stop"
echo "=================================="
python run.py