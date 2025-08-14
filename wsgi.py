"""
WSGI configuration for Heroku deployment
"""
import os

# Configurar variáveis de ambiente para produção
os.environ.setdefault('FLASK_ENV', 'production')

# Import the ultra-simplified Flask app
from heroku_app_simple import app

# This is what Heroku will use
application = app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)