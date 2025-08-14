import os
import json
import logging
import requests
import qrcode
import base64
from io import BytesIO
from typing import Dict, Any, Optional
from dataclasses import dataclass
import uuid
from datetime import datetime, timedelta

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class IronPaymentData:
    """Dados necessários para pagamento Iron Pay"""
    name: str
    email: str
    cpf: str
    phone: str
    amount: float
    description: str
    street_name: str = "Não informado"
    number: str = "s/n"
    city: str = "São Paulo"
    state: str = "SP"
    zip_code: str = "01000000"

@dataclass
class IronPaymentResponse:
    """Resposta da Iron Pay API"""
    transaction_hash: str
    pix_code: str
    pix_qr_code: str
    status: str
    amount: float
    expires_at: Optional[str] = None

class IronPayAPI:
    """
    Cliente para Iron Pay API - PIX Real
    """
    
    def __init__(self, api_token: Optional[str] = None, timeout: int = 30):
        """Inicializar Iron Pay API"""
        self.API_URL = "https://api.ironpayapp.com.br"
        self.timeout = timeout
        
        # Token fornecido pelo usuário
        self.api_token = api_token or "xYipgGdsLKk2779ZQHqpfm0TfZqJqJP8q5iRj272pogLoOhV5dJjY7jpftrD"
        
        # Configurar session
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "IronPay-IBGE-Client/1.0"
        })
        
        logger.info(f"✅ Iron Pay API initialized - URL: {self.API_URL}")
        
    def create_pix_payment(self, data: IronPaymentData) -> IronPaymentResponse:
        """Criar pagamento PIX via Iron Pay"""
        
        # Validar e limpar dados
        cpf_clean = ''.join(filter(str.isdigit, data.cpf))
        if len(cpf_clean) != 11:
            raise ValueError(f"CPF inválido: {data.cpf}")
            
        phone_clean = ''.join(filter(str.isdigit, data.phone))
        if len(phone_clean) < 10:
            phone_clean = "11999999999"
            
        amount_cents = int(data.amount * 100)  # Iron Pay usa centavos
        
        # Hashes específicos da conta do usuário (conforme documentação)
        product_hash = "jrddtst9rp"
        offer_hash = "vduc64lrsq"
        
        # Preparar payload conforme documentação Iron Pay
        payment_data = {
            "amount": amount_cents,
            "offer_hash": offer_hash,
            "payment_method": "pix",
            "customer": {
                "name": data.name.strip().upper(),
                "email": data.email.strip().lower(),
                "phone_number": phone_clean,
                "document": cpf_clean,
                "street_name": data.street_name,
                "number": data.number,
                "neighborhood": "Centro",
                "city": data.city,
                "state": data.state,
                "zip_code": data.zip_code
            },
            "cart": [{
                "product_hash": product_hash,
                "title": data.description,
                "cover": None,
                "price": amount_cents,
                "quantity": 1,
                "operation_type": 1,
                "tangible": False,
                "product_id": 6561,
                "offer_id": 9535
            }],
            "installments": 1,
            "expire_in_days": 1,
            "transaction_origin": "api",
            "tracking": {
                "src": "",
                "utm_source": "",
                "utm_medium": "",
                "utm_campaign": "",
                "utm_term": "",
                "utm_content": ""
            }
        }
        
        logger.info(f"🔄 Criando PIX Iron Pay REAL - Valor: R${data.amount:.2f}, Cliente: {data.name}")
        
        try:
            # Fazer requisição para Iron Pay API REAL
            response = self.session.post(
                f"{self.API_URL}/api/public/v1/transactions",
                params={"api_token": self.api_token},
                json=payment_data,
                timeout=self.timeout
            )
            
            logger.info(f"📡 Iron Pay Response: HTTP {response.status_code}")
            
            if response.status_code in [200, 201]:
                response_data = response.json()
                logger.info(f"✅ Iron Pay Success: {response_data}")
                
                # Extrair dados da resposta
                transaction_hash = response_data.get("hash")
                pix_data = response_data.get("pix", {})
                pix_code = pix_data.get("pix_qr_code", "")
                pix_expiration = pix_data.get("pix_expiration_date", "")
                
                if not transaction_hash:
                    raise Exception("Iron Pay não retornou hash da transação")
                
                # Gerar QR code se necessário
                pix_qr_code = ""
                if pix_code:
                    pix_qr_code = self._generate_qr_code_base64(pix_code)
                
                logger.info(f"🎉 PIX REAL criado! Hash: {transaction_hash}")
                
                return IronPaymentResponse(
                    transaction_hash=transaction_hash,
                    pix_code=pix_code or "",
                    pix_qr_code=pix_qr_code,
                    status=response_data.get("payment_status", "pending"),
                    amount=data.amount,
                    expires_at=pix_expiration
                )
            else:
                error_msg = f"Iron Pay API error: HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f" - {error_data}"
                    logger.error(f"❌ Iron Pay Error Response: {error_data}")
                except:
                    error_msg += f" - {response.text}"
                    logger.error(f"❌ Iron Pay Error Text: {response.text}")
                
                raise Exception(error_msg)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Iron Pay connection error: {e}")
            raise Exception(f"Iron Pay connection error: {e}")
        except Exception as e:
            logger.error(f"❌ Iron Pay error: {e}")
            raise
            
    def check_payment_status(self, transaction_hash: str) -> Dict[str, Any]:
        """Verificar status do pagamento"""
        try:
            response = self.session.get(
                f"{self.API_URL}/api/public/v1/transactions/{transaction_hash}",
                params={"api_token": self.api_token},
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'status': data.get('payment_status', 'pending'),
                    'transaction_hash': transaction_hash,
                    'paid': data.get('payment_status') == 'paid',
                    'amount': data.get('amount', 0) / 100,
                    'customer': data.get('customer', {}),
                    'created_at': data.get('created_at', ''),
                    'updated_at': data.get('updated_at', '')
                }
            else:
                logger.warning(f"⚠️ Erro ao verificar status Iron Pay: HTTP {response.status_code}")
                return {
                    'status': 'pending',
                    'transaction_hash': transaction_hash,
                    'paid': False
                }
                
        except Exception as e:
            logger.error(f"❌ Erro ao verificar status: {e}")
            return {
                'status': 'error',
                'transaction_hash': transaction_hash,
                'paid': False,
                'error': str(e)
            }
    
    def _generate_qr_code_base64(self, pix_code: str) -> str:
        """Gerar QR code em base64"""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(pix_code)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            return f"data:image/png;base64,{img_base64}"
            
        except Exception as e:
            logger.error(f"❌ Error generating QR code: {e}")
            return ""

def create_iron_pay_client() -> IronPayAPI:
    """Factory function para criar instância da Iron Pay API"""
    return IronPayAPI()