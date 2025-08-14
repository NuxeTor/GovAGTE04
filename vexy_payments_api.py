import os
import requests
import logging
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Dict, Any

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class VexyPaymentData:
    """Dados necessários para criar um pagamento PIX via Vexy Payments"""
    name: str
    email: str
    document: str  # CPF sem formatação
    amount: float
    external_id: str  # ID único da transação
    description: str
    callback_url: str = "https://webhook.site/unique-id"

@dataclass
class VexyPaymentResponse:
    """Resposta da API Vexy Payments"""
    success: bool
    transaction_id: Optional[str] = None
    amount: Optional[float] = None
    pix_code: Optional[str] = None
    qr_code: Optional[str] = None
    status: Optional[str] = None
    error_message: Optional[str] = None

class VexyPaymentsAPI:
    """Cliente para a API Vexy Payments"""
    
    def __init__(self, client_id: str, client_secret: str, base_url: str = "https://api.vexypayments.com"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url.rstrip('/')
        self.auth_token = None
        
        logger.info(f"✅ Vexy Payments API initialized - URL: {self.base_url}")
        logger.info(f"✅ Client ID: {self.client_id[:12]}***")
    
    def authenticate(self) -> bool:
        """Autentica na API e obtém token JWT"""
        try:
            auth_url = f"{self.base_url}/api/auth/login"
            
            # IMPORTANTE: Use "client_id" e "client_secret" (com underscore)
            payload = {
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            
            logger.info(f"🔐 Autenticando na Vexy Payments: {auth_url}")
            
            response = requests.post(auth_url, json=payload, timeout=30)
            
            logger.info(f"📡 Status autenticação: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                # IMPORTANTE: O token está no campo "token", não "accessToken"
                self.auth_token = data.get('token')
                
                if self.auth_token:
                    logger.info("✅ Autenticação Vexy Payments bem-sucedida")
                    return True
                else:
                    logger.error("❌ Token não encontrado na resposta")
                    return False
            else:
                logger.error(f"❌ Erro de autenticação: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro na autenticação: {e}")
            return False
    
    def create_deposit(self, payment_data: VexyPaymentData) -> VexyPaymentResponse:
        """Cria um depósito PIX via Vexy Payments"""
        
        # Autenticar se necessário
        if not self.auth_token:
            if not self.authenticate():
                return VexyPaymentResponse(
                    success=False,
                    error_message="Falha na autenticação"
                )
        
        try:
            deposit_url = f"{self.base_url}/api/payments/deposit"
            
            # Limpar CPF (apenas números)
            clean_document = ''.join(filter(str.isdigit, payment_data.document))
            
            payload = {
                "amount": payment_data.amount,
                "external_id": payment_data.external_id,
                "clientCallbackUrl": payment_data.callback_url,
                "payer": {
                    "name": payment_data.name,
                    "email": payment_data.email,
                    "document": clean_document
                }
            }
            
            headers = {
                "Authorization": f"Bearer {self.auth_token}",
                "Content-Type": "application/json"
            }
            
            logger.info(f"💰 Criando depósito Vexy: {deposit_url}")
            logger.info(f"💰 Dados: {payload}")
            
            response = requests.post(deposit_url, json=payload, headers=headers, timeout=30)
            
            logger.info(f"📡 Status criação depósito: {response.status_code}")
            logger.info(f"📡 Resposta: {response.text}")
            
            if response.status_code == 200 or response.status_code == 201:
                data = response.json()
                
                # Extrair dados da estrutura específica da Vexy Payments
                qr_response = data.get('qrCodeResponse', {})
                
                # O QR code e transaction ID estão dentro de qrCodeResponse
                transaction_id = qr_response.get('transactionId')
                qr_code = qr_response.get('qrcode')
                amount = qr_response.get('amount')
                status = qr_response.get('status', 'PENDING').lower()
                
                logger.info(f"📋 Dados extraídos Vexy:")
                logger.info(f"   Transaction ID: {transaction_id}")
                logger.info(f"   QR Code: {qr_code[:50] if qr_code else 'None'}...")
                logger.info(f"   Amount: {amount}")
                logger.info(f"   Status: {status}")
                
                return VexyPaymentResponse(
                    success=True,
                    transaction_id=transaction_id,
                    amount=amount,
                    pix_code=qr_code,  # Na Vexy, o QR code É o código PIX
                    qr_code=qr_code,
                    status=status
                )
            else:
                error_msg = f"Erro HTTP {response.status_code}: {response.text}"
                logger.error(f"❌ {error_msg}")
                return VexyPaymentResponse(
                    success=False,
                    error_message=error_msg
                )
                
        except Exception as e:
            error_msg = f"Erro na criação do depósito: {e}"
            logger.error(f"❌ {error_msg}")
            return VexyPaymentResponse(
                success=False,
                error_message=error_msg
            )
    
    def check_payment_status(self, transaction_id: str) -> Dict[str, Any]:
        """Verifica o status de um pagamento"""
        # Nota: A Vexy Payments usa webhooks para notificações
        # Este método retorna status padrão
        return {
            "status": "pending",
            "transaction_id": transaction_id
        }

class VexyPaymentAPICompatibility:
    """Wrapper para manter compatibilidade com a interface existente"""
    
    def __init__(self, client_id: str, client_secret: str):
        self.vexy_api = VexyPaymentsAPI(client_id, client_secret)
    
    def create_pix_payment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Interface compatível com formato anterior para facilitar migração"""
        
        # Validar campos obrigatórios
        required_fields = ['name', 'email', 'cpf', 'amount']
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Campo obrigatório ausente: {field}")
        
        # Gerar ID único para a transação
        external_id = f"ibge_{data['cpf'].replace('.', '').replace('-', '')}_{int(datetime.now().timestamp())}"
        
        # Converter para formato Vexy Payments
        payment_data = VexyPaymentData(
            name=data['name'],
            email=data['email'],
            document=data['cpf'],
            amount=float(data['amount']),
            external_id=external_id,
            description=data.get('description', 'Taxa de Inscrição - IBGE Trabalhe Conosco'),
            callback_url=data.get('callback_url', 'https://webhook.site/unique-id')
        )
        
        # Criar pagamento
        vexy_response = self.vexy_api.create_deposit(payment_data)
        
        if vexy_response.success:
            # Retornar no formato esperado pelo frontend
            return {
                'success': True,
                'id': vexy_response.transaction_id,
                'hash': vexy_response.transaction_id,  # Usar transaction_id como hash
                'pixCode': vexy_response.pix_code,
                'pixQrCode': vexy_response.qr_code,
                'expiresAt': None,  # Vexy não retorna data de expiração específica
                'status': vexy_response.status,
                'provider': 'Vexy Payments'
            }
        else:
            return {
                'success': False,
                'error': vexy_response.error_message
            }
    
    def check_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """Verificar status do pagamento mantendo interface compatível"""
        return self.vexy_api.check_payment_status(payment_id)

def create_vexy_payments_provider() -> VexyPaymentAPICompatibility:
    """Factory function para criar instância da API"""
    client_id = os.getenv('VEXY_CLIENT_ID', 'homecler_9ECDBAEA')
    client_secret = os.getenv('VEXY_CLIENT_SECRET', '7e6844322408f24bf810da673bd8fff264c03dc7afd7e8e23f58b9897336afec2938614ca1cf63a1164deba77a06845407a7')
    
    return VexyPaymentAPICompatibility(client_id, client_secret)

def create_payment_api() -> VexyPaymentAPICompatibility:
    """Factory function principal para criar instância da API de pagamentos"""
    return create_vexy_payments_provider()

# Exemplo de uso
if __name__ == "__main__":
    # Criar cliente da API
    vexy_api = create_vexy_payments_provider()
    
    # Dados do pagamento
    payment_data = {
        'name': "CLIENTE TESTE",
        'email': "cliente@exemplo.com", 
        'cpf': "12345678901",
        'amount': 87.40
    }
    
    # Criar PIX
    response = vexy_api.create_pix_payment(payment_data)
    
    if response.get('success'):
        print(f"✅ PIX criado com sucesso!")
        print(f"Transaction ID: {response['id']}")
        print(f"Código PIX: {response['pixCode']}")
    else:
        print(f"❌ Erro: {response.get('error')}")