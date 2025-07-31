import requests
import base64
import json
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# Configurar logging para produção
import os
if os.environ.get('FLASK_ENV') == 'production':
    logging.basicConfig(level=logging.ERROR)
else:
    logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

@dataclass
class Customer:
    """Dados do cliente para pagamento"""
    name: str
    email: str
    phone: str
    cpf: str

@dataclass
class PaymentItem:
    """Item do pagamento"""
    title: str
    quantity: int = 1
    unit_price: int = 8740  # Em centavos
    tangible: bool = False

@dataclass
class PixTransaction:
    """Dados da transação PIX"""
    id: str
    status: str
    amount: int
    qr_code: str
    expires_at: str
    created_at: str

class NovaEraAPI:
    """
    Cliente para API Nova Era de pagamentos PIX
    """
    
    def __init__(self, secret_key: str, public_key: str):
        self.secret_key = secret_key
        self.public_key = public_key
        self.base_url = "https://api.novaera-pagamentos.com/api/v1"
        
    def _get_auth_token(self) -> str:
        """Gera token de autenticação Basic Auth"""
        credentials = f"{self.secret_key}:{self.public_key}"
        token = base64.b64encode(credentials.encode()).decode()
        return f"Basic {token}"
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Faz requisição para a API"""
        url = f"{self.base_url}{endpoint}"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": self._get_auth_token()
        }
        
        logger.debug(f"Making {method} request to {url}")
        
        try:
            if method.upper() == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            else:
                raise ValueError(f"Método HTTP não suportado: {method}")
            
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response body: {response.text}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON: {e}")
            raise
    
    def create_pix_transaction(self, customer: Customer, amount: int, description: str = "Taxa de Inscrição - Correios Contrata") -> PixTransaction:
        """
        Cria uma nova transação PIX
        
        Args:
            customer: Dados do cliente
            amount: Valor em centavos (ex: 8740 = R$ 87,40)
            description: Descrição do pagamento
        
        Returns:
            PixTransaction: Dados da transação criada
        """
        
        # Preparar dados do cliente
        customer_data = {
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone,
            "document": {
                "number": customer.cpf.replace(".", "").replace("-", ""),
                "type": "cpf"
            }
        }
        
        # Preparar item do pagamento
        items = [
            {
                "tangible": False,
                "quantity": 1,
                "unitPrice": amount,
                "title": description
            }
        ]
        
        # Dados da transação
        transaction_data = {
            "customer": customer_data,
            "items": items,
            "postbackUrl": "https://webhook.site/your-webhook-url",  # URL para receber notificações
            "amount": amount,
            "paymentMethod": "pix"
        }
        
        logger.info(f"Criando transação PIX para {customer.name} - Valor: R$ {amount/100:.2f}")
        
        try:
            response = self._make_request("POST", "/transactions", transaction_data)
            
            if response.get("success"):
                data = response["data"]
                return PixTransaction(
                    id=str(data["id"]),
                    status=data["status"],
                    amount=data["amount"],
                    qr_code=data["pix"]["qrcode"],
                    expires_at=data["pix"]["expirationDate"],  # Campo correto da API
                    created_at=data["createdAt"]
                )
            else:
                error_msg = response.get("error", {}).get("message", "Erro desconhecido")
                raise Exception(f"Erro da API: {error_msg}")
                
        except Exception as e:
            logger.error(f"Erro ao criar transação PIX: {e}")
            raise
    
    def get_transaction_status(self, transaction_id: str) -> Dict[str, Any]:
        """
        Consulta o status de uma transação
        
        Args:
            transaction_id: ID da transação
        
        Returns:
            Dict: Dados da transação
        """
        logger.info(f"Consultando status da transação: {transaction_id}")
        
        try:
            response = self._make_request("GET", f"/transactions/{transaction_id}")
            
            if response.get("success"):
                return response["data"]
            else:
                error_msg = response.get("error", {}).get("message", "Erro desconhecido")
                raise Exception(f"Erro da API: {error_msg}")
                
        except Exception as e:
            logger.error(f"Erro ao consultar transação: {e}")
            raise

# Função auxiliar para criar instância da API
def create_nova_era_client() -> NovaEraAPI:
    """Cria cliente da API Nova Era com as credenciais fornecidas"""
    secret_key = "sk_uluAT1O9I6FGTQAcXzccr2H_eAQ9IOzYoY_LLDfR8U6Uv2Xb"
    public_key = "pk_E5SWGB_rZ-mZowMITdSr5w8zhOdY8TDImLhOM-s9gmJPoc9x"
    
    return NovaEraAPI(secret_key, public_key)

# Função de teste
def test_api():
    """Função para testar a API"""
    try:
        api = create_nova_era_client()
        
        # Dados de teste
        customer = Customer(
            name="RIZIA REGIA DA SILVA RODRIGUES MAGALHAES",
            email="rizia@teste.com",
            phone="(11) 99999-9999",
            cpf="011.011.011-05"
        )
        
        # Criar transação
        transaction = api.create_pix_transaction(customer, 8740)
        
        print(f"Transação criada com sucesso!")
        print(f"ID: {transaction.id}")
        print(f"Status: {transaction.status}")
        print(f"QR Code: {transaction.qr_code[:50]}...")
        print(f"Expira em: {transaction.expires_at}")
        
        return transaction
        
    except Exception as e:
        print(f"Erro no teste: {e}")
        return None

if __name__ == "__main__":
    test_api()