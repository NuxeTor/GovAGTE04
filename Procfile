
web: python -c "import os; os.system('pkill -9 -f gunicorn'); import time; time.sleep(1)" && gunicorn --bind 0.0.0.0:5000 --workers 1 --timeout 30 main:app
