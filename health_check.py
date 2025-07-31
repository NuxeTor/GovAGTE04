"""
Health check script for Heroku deployment
"""
import requests
import sys
import os

def check_health():
    """Check if the application is healthy"""
    try:
        # Get the URL from environment or use localhost
        url = os.environ.get('HEROKU_APP_URL', 'http://localhost:5000')
        if not url.endswith('/'):
            url += '/'
            
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            print("✅ Application is healthy")
            return True
        else:
            print(f"❌ Application returned status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    if check_health():
        sys.exit(0)
    else:
        sys.exit(1)