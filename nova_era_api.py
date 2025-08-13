"""
Nova Era API Integration
Real PIX payment processing with user's credentials
"""
import os
import base64
import requests
import logging
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class Customer:
    """Customer data structure for Nova Era API"""
    def __init__(self, name: str, email: str, phone: str, cpf: str):
        self.name = name
        self.email = email
        self.phone = phone
        self.cpf = cpf.replace('.', '').replace('-', '')  # Clean CPF

class Transaction:
    """Transaction response structure"""
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id')
        self.status = data.get('status')
        self.amount = data.get('amount')
        self.qr_code = data.get('pix', {}).get('qrcode')
        self.expires_at = data.get('pix', {}).get('expires_at')
        self.created_at = data.get('created_at')
        self.paid_at = data.get('paid_at')

class NovaEraAPI:
    """
    Cliente para API Nova Era de pagamentos PIX
    Usando credenciais reais do usuário
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
        """Faz requisição para a API Nova Era"""
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
            logger.error(f"Erro na requisição para Nova Era API: {e}")
            raise Exception(f"Erro de comunicação com a API: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado: {e}")
            raise
    
    def create_pix_transaction(self, customer: Customer, amount_cents: int, description: str = "Taxa de Inscrição - IBGE Trabalhe Conosco") -> Transaction:
        """
        Cria uma nova transação PIX
        
        Args:
            customer: Dados do cliente
            amount_cents: Valor em centavos (ex: 8740 = R$ 87,40)
            description: Descrição da transação
            
        Returns:
            Transaction: Objeto com dados da transação criada
        """
        payload = {
            "customer": {
                "name": customer.name,
                "email": customer.email,
                "phone": customer.phone,
                "document": {
                    "number": customer.cpf,
                    "type": "cpf"
                }
            },
            "items": [
                {
                    "tangible": False,
                    "quantity": 1,
                    "unitPrice": amount_cents,
                    "title": description
                }
            ],
            "postbackUrl": "https://webhook-site.com/nova-era-webhook",  # URL para receber notificações
            "amount": amount_cents,
            "paymentMethod": "pix"
        }
        
        response = self._make_request("POST", "/transactions", payload)
        
        if response.get("success"):
            return Transaction(response["data"])
        else:
            error_msg = response.get("error", {}).get("message", "Erro desconhecido")
            raise Exception(f"Erro da API Nova Era: {error_msg}")
    
    def get_transaction_status(self, transaction_id: str) -> Dict[str, Any]:
        """
        Consulta o status de uma transação
        
        Args:
            transaction_id: ID da transação
            
        Returns:
            Dict: Dados da transação atualizada
        """
        response = self._make_request("GET", f"/transactions/{transaction_id}")
        
        if response.get("success"):
            return response["data"]
        else:
            error_msg = response.get("error", {}).get("message", "Erro desconhecido")
            raise Exception(f"Erro da API Nova Era: {error_msg}")

def create_nova_era_client() -> NovaEraAPI:
    """
    Cria cliente da API Nova Era com as credenciais do usuário
    """
    # Credenciais reais fornecidas pelo usuário
    secret_key = os.environ.get("NOVA_ERA_SECRET_KEY", "sk_uluAT1O9I6FGTQAcXzccr2H_eAQ9IOzYoY_LLDfR8U6Uv2Xb")
    public_key = os.environ.get("NOVA_ERA_PUBLIC_KEY", "pk_E5SWGB_rZ-mZowMITdSr5w8zhOdY8TDImLhOM-s9gmJPoc9x")
    
    return NovaEraAPI(secret_key, public_key)