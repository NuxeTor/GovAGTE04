
"""
For4Payments PIX API - Integração para o projeto
"""

import os
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class PaymentRequestData:
    """Dados necessários para criar um pagamento PIX"""
    name: str
    email: str
    cpf: str
    amount: int  # Valor em centavos
    phone: Optional[str] = None
    description: Optional[str] = None

@dataclass
class PaymentResponse:
    """Resposta da criação de pagamento PIX"""
    id: str
    pix_code: str
    pix_qr_code: str
    expires_at: str
    status: str

class For4PaymentsAPI:
    """
    Classe principal para integração com a API For4Payments
    
    URL Base da API: https://app.for4payments.com.br/api/v1
    
    Endpoints utilizados:
    - POST /transaction.purchase - Criar pagamento PIX
    - GET /transaction.getPayment?id={payment_id} - Verificar status do pagamento
    """
    
    def __init__(self, secret_key: str):
        self.API_URL = "https://app.for4payments.com.br/api/v1"
        self.secret_key = secret_key
        
        # Validar chave de API
        if not secret_key or len(secret_key) < 10:
            raise ValueError("Token de autenticação inválido")
    
    def _get_headers(self) -> Dict[str, str]:
        """Headers padrão para as requisições"""
        return {
            "Authorization": self.secret_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Referer": "https://voabrasil2025.org/pagamento",
            "X-Requested-With": "XMLHttpRequest",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
        }
    
    def create_pix_payment(self, data: PaymentRequestData) -> PaymentResponse:
        """
        Criar um pagamento PIX
        
        Args:
            data: Dados do pagamento (PaymentRequestData)
            
        Returns:
            PaymentResponse: Dados do pagamento criado
            
        Raises:
            ValueError: Para erros de validação
            requests.exceptions.RequestException: Para erros de rede/API
        """
        
        # Validar campos obrigatórios
        if not data.name or not data.name.strip():
            raise ValueError("Nome é obrigatório")
        if not data.email or not data.email.strip():
            raise ValueError("Email é obrigatório")
        if not data.cpf or not data.cpf.strip():
            raise ValueError("CPF é obrigatório")
        if not data.amount or data.amount <= 0:
            raise ValueError("Valor é obrigatório e deve ser maior que zero")
        
        # Validar e formatar CPF
        cpf = ''.join(filter(str.isdigit, data.cpf))
        if len(cpf) != 11:
            raise ValueError("CPF inválido")
        
        # Validar email
        if "@" not in data.email:
            raise ValueError("Email inválido")
        
        # Validar valor
        amount = int(data.amount)
        if amount <= 0:
            raise ValueError("Valor do pagamento deve ser maior que zero")
        
        # Formatar telefone
        phone = ''.join(filter(str.isdigit, data.phone)) if data.phone else "11999999999"
        
        # Dados do pagamento para a API
        payment_data = {
            "name": data.name,
            "email": data.email,
            "cpf": cpf,
            "phone": phone,
            "paymentMethod": "PIX",
            "amount": amount,  # Valor em centavos
            "traceable": True,
            "items": [
                {
                    "title": data.description or "Taxa de Inscrição - PNAE",
                    "quantity": 1,
                    "unitPrice": amount,  # Valor em centavos
                    "tangible": False
                }
            ],
            "cep": "77828-558",
            "street": "Rua Exemplo",
            "number": "123",
            "complement": "Apto 101",
            "district": "Centro",
            "city": "São Paulo",
            "state": "SP",
            "utmQuery": "",
            "checkoutUrl": "",
            "referrerUrl": "",
            "externalId": f"pnae-{int(datetime.now().timestamp())}",
            "postbackUrl": "",
            "fingerPrints": []
        }
        
        try:
            print(f"Enviando requisição para: {self.API_URL}/transaction.purchase")
            print(f"Payload: {json.dumps(payment_data, indent=2)}")
            
            response = requests.post(
                f"{self.API_URL}/transaction.purchase",
                json=payment_data,
                headers=self._get_headers(),
                timeout=30
            )
            
            print(f"Status da resposta: {response.status_code}")
            print(f"Resposta: {response.text}")
            
            if response.status_code != 200:
                error_message = "Erro ao processar pagamento"
                if response.status_code == 401:
                    error_message = "Falha na autenticação com a API For4Payments. Verifique a chave de API."
                elif response.text:
                    try:
                        error_data = response.json()
                        error_message = (
                            error_data.get("message") or 
                            error_data.get("error") or 
                            "Erro desconhecido"
                        )
                    except:
                        error_message = response.text
                
                raise requests.exceptions.RequestException(f"API Error: {error_message}")
            
            response_data = response.json()
            
            # Extrair dados do PIX com fallbacks
            pix_code = (
                response_data.get("pix", {}).get("code") or
                response_data.get("pixData", {}).get("copyPaste") or
                response_data.get("pixCode") or
                response_data.get("copy_paste") or
                response_data.get("code")
            )
            
            pix_qr_code = (
                response_data.get("pix", {}).get("qrCode") or
                response_data.get("pix", {}).get("base64Image") or
                response_data.get("qrCode", {}).get("imageUrl") or
                response_data.get("qr_code_image") or
                response_data.get("pixQrCode")
            )
            
            expires_at = (
                response_data.get("expiration") or
                response_data.get("expiresAt") or
                (datetime.now() + timedelta(minutes=30)).isoformat()
            )
            
            status = response_data.get("status", "pending").lower()
            
            payment_id = (
                response_data.get("id") or
                response_data.get("transactionId") or
                response_data.get("_id") or
                f"txn-{int(datetime.now().timestamp())}"
            )
            
            return PaymentResponse(
                id=payment_id,
                pix_code=pix_code,
                pix_qr_code=pix_qr_code,
                expires_at=expires_at,
                status=status
            )
            
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {str(e)}")
            raise
        except Exception as e:
            print(f"Erro inesperado: {str(e)}")
            raise
    
    def check_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """
        Verificar o status de um pagamento
        
        Args:
            payment_id: ID do pagamento
            
        Returns:
            Dict contendo status, pixQrCode e pixCode (se disponível)
        """
        
        try:
            url = f"{self.API_URL}/transaction.getPayment?id={payment_id}"
            print(f"Verificando status do pagamento {payment_id}...")
            print(f"URL: {url}")
            
            response = requests.get(
                url,
                headers=self._get_headers(),
                timeout=30
            )
            
            print(f"Status da resposta: {response.status_code}")
            
            if response.status_code == 404:
                print(f"Pagamento {payment_id} não encontrado")
                return {"status": "pending"}
            
            if response.status_code != 200:
                print(f"Erro ao verificar status: {response.status_code}")
                return {"status": "pending"}
            
            payment_data = response.json()
            print(f"Dados do pagamento: {json.dumps(payment_data, indent=2)}")
            
            # Mapeamento de status
            status_mapping = {
                "pending": "pending",
                "processing": "pending",
                "approved": "completed",
                "completed": "completed",
                "paid": "completed",
                "expired": "failed",
                "failed": "failed",
                "canceled": "cancelled",
                "cancelled": "cancelled"
            }
            
            current_status = payment_data.get("status", "pending").lower()
            mapped_status = status_mapping.get(current_status, "pending")
            
            # Extrair códigos PIX
            pix_code = (
                payment_data.get("pix", {}).get("code") or
                payment_data.get("pixData", {}).get("copyPaste") or
                payment_data.get("pixCode") or
                payment_data.get("copy_paste") or
                payment_data.get("code")
            )
            
            pix_qr_code = (
                payment_data.get("pix", {}).get("qrCode") or
                payment_data.get("pix", {}).get("base64Image") or
                payment_data.get("qrCode", {}).get("imageUrl") or
                payment_data.get("qr_code_image") or
                payment_data.get("pixQrCode")
            )
            
            result = {"status": mapped_status}
            if pix_code:
                result["pixCode"] = pix_code
            if pix_qr_code:
                result["pixQrCode"] = pix_qr_code
            
            return result
            
        except Exception as e:
            print(f"Erro ao verificar status do pagamento: {str(e)}")
            return {"status": "pending"}

def create_payment_api() -> For4PaymentsAPI:
    """
    Factory function para criar uma instância da API
    
    Returns:
        For4PaymentsAPI: Instância configurada da API
        
    Raises:
        ValueError: Se a chave de API não estiver configurada
    """
    
    secret_key = os.getenv("FOR4PAYMENTS_SECRET_KEY")
    
    if not secret_key:
        raise ValueError("Chave de API FOR4PAYMENTS_SECRET_KEY não configurada no ambiente")
    
    if len(secret_key) < 10:
        raise ValueError("Chave de API FOR4PAYMENTS_SECRET_KEY parece ser inválida")
    
    return For4PaymentsAPI(secret_key)
