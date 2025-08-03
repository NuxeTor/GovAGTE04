
web: gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 30 --max-requests 1000 --max-requests-jitter 50 --preload --access-logfile - --error-logfile - main:app
