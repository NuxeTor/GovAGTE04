import os
import logging
from flask import Flask, render_template, request, jsonify

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

@app.route('/')
def index():
    """Main page showing the Mais Agentes da Educação program"""
    return render_template('index.html')

@app.route('/acesso-informacao')
def acesso_informacao():
    """Access to Information page"""
    return render_template('index.html', page_title="Acesso à Informação")

@app.route('/acoes-programas')
def acoes_programas():
    """Actions and Programs page"""
    return render_template('index.html', page_title="Ações e Programas")

@app.route('/programas')
def programas():
    """Programs page"""
    return render_template('index.html', page_title="Programas")

@app.route('/bolsas-auxilios')
def bolsas_auxilios():
    """Scholarships and Aid page"""
    return render_template('index.html', page_title="Bolsas e Auxílios")

@app.route('/lista-programas')
def lista_programas():
    """Programs List page"""
    return render_template('index.html', page_title="Lista de Programas")

@app.route('/search')
def search():
    """Search functionality"""
    query = request.args.get('q', '')
    # In a real implementation, this would search through content
    return jsonify({'query': query, 'results': []})

@app.route('/login')
def login():
    """Login page (mock interface)"""
    return render_template('index.html', page_title="Login")

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('index.html', page_title="Página não encontrada"), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('index.html', page_title="Erro interno do servidor"), 500

if __name__ == '__main__':
    # Run the app on port 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
