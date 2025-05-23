import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Define models directly in app.py to avoid import issues
class Program(db.Model):
    """Model for government education programs"""
    __tablename__ = 'programs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ministry = db.Column(db.String(100), nullable=False)
    program_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='active')
    published_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Program {self.title}>'

class Position(db.Model):
    """Model for job positions within programs"""
    __tablename__ = 'positions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    requirements = db.Column(db.Text)
    salary_min = db.Column(db.Numeric(10, 2))
    salary_max = db.Column(db.Numeric(10, 2))
    workload_hours = db.Column(db.Integer)
    work_type = db.Column(db.String(50))
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    
    def __repr__(self):
        return f'<Position {self.name}>'

# Create tables
with app.app_context():
    db.create_all()

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
