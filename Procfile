
web: gunicorn --bind 0.0.0.0:5000 --worker-class sync --workers 1 --timeout 120 --keep-alive 2 --max-requests 500 --preload main:app
