
web: gunicorn --bind 0.0.0.0:5000 --workers 1 --timeout 30 --keep-alive 2 --max-requests 500 --max-requests-jitter 50 --preload main:app
