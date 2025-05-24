import pandas as pd
import requests
from geopy.distance import geodesic
import os
import logging

class EscolaService:
    def __init__(self):
        self.escolas_df = None
        self.token_api = "67a8853ca627a5164edec7831f2bf7f2114edfced186eb70eb00db219a05b342"
        self.carregar_escolas()
    
    def carregar_escolas(self):
        """Carrega os dados das escolas do arquivo Excel"""
        try:
            arquivo_excel = "attached_assets/escolas.xlsx"
            if os.path.exists(arquivo_excel):
                # Tenta ler o arquivo Excel
                self.escolas_df = pd.read_excel(arquivo_excel)
                logging.info(f"Carregadas {len(self.escolas_df)} escolas do arquivo Excel")
                
                # Renomear colunas para padronizar
                colunas_esperadas = ['Escola', 'Codigo_INEP', 'UF', 'Municipio', 'Endereco', 'Latitude', 'Longitude']
                if len(self.escolas_df.columns) == len(colunas_esperadas):
                    self.escolas_df.columns = colunas_esperadas
                
                # Converter coordenadas para float
                self.escolas_df['Latitude'] = pd.to_numeric(self.escolas_df['Latitude'], errors='coerce')
                self.escolas_df['Longitude'] = pd.to_numeric(self.escolas_df['Longitude'], errors='coerce')
                
                # Remover escolas sem coordenadas válidas
                self.escolas_df = self.escolas_df.dropna(subset=['Latitude', 'Longitude'])
                
            else:
                logging.warning(f"Arquivo {arquivo_excel} não encontrado")
                self.criar_dados_exemplo()
                
        except Exception as e:
            logging.error(f"Erro ao carregar escolas: {e}")
            self.criar_dados_exemplo()
    
    def criar_dados_exemplo(self):
        """Cria dados de exemplo caso o arquivo não seja encontrado"""
        dados_exemplo = [
            {
                'Escola': 'Escola Municipal João Silva',
                'Codigo_INEP': '23000001',
                'UF': 'SP',
                'Municipio': 'São Paulo',
                'Endereco': 'Rua das Flores, 123 - Centro',
                'Latitude': -23.5505,
                'Longitude': -46.6333
            },
            {
                'Escola': 'Escola Municipal Maria Santos',
                'Codigo_INEP': '23000002',
                'UF': 'SP',
                'Municipio': 'São Paulo',
                'Endereco': 'Av. Principal, 456 - Bairro Novo',
                'Latitude': -23.5489,
                'Longitude': -46.6388
            },
            {
                'Escola': 'Escola Municipal Pedro Oliveira',
                'Codigo_INEP': '23000003',
                'UF': 'SP',
                'Municipio': 'São Paulo',
                'Endereco': 'Rua da Educação, 789 - Vila Esperança',
                'Latitude': -23.5520,
                'Longitude': -46.6280
            }
        ]
        self.escolas_df = pd.DataFrame(dados_exemplo)
        logging.info("Usando dados de exemplo das escolas")
    
    def obter_coordenadas_cep(self, cep):
        """Obtém latitude e longitude do CEP usando a API AwesomeApi"""
        try:
            # Remove formatação do CEP
            cep_limpo = cep.replace('-', '').replace('.', '')
            
            url = f"https://cep.awesomeapi.com.br/json/{cep_limpo}?token={self.token_api}"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            dados = response.json()
            
            if 'lat' in dados and 'lng' in dados:
                return float(dados['lat']), float(dados['lng']), dados
            else:
                logging.error(f"Coordenadas não encontradas para o CEP {cep}")
                return None, None, None
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro na requisição da API: {e}")
            return None, None, None
        except Exception as e:
            logging.error(f"Erro ao obter coordenadas do CEP {cep}: {e}")
            return None, None, None
    
    def calcular_distancia(self, lat1, lng1, lat2, lng2):
        """Calcula a distância entre duas coordenadas em quilômetros"""
        try:
            return geodesic((lat1, lng1), (lat2, lng2)).kilometers
        except Exception as e:
            logging.error(f"Erro ao calcular distância: {e}")
            return float('inf')
    
    def buscar_escolas_proximas(self, cep, limite=3):
        """Busca escolas próximas ao CEP informado"""
        try:
            # Obter coordenadas do CEP
            lat_cep, lng_cep, dados_cep = self.obter_coordenadas_cep(cep)
            
            if lat_cep is None or lng_cep is None:
                return None, "Erro ao obter coordenadas do CEP"
            
            if self.escolas_df is None or self.escolas_df.empty:
                return None, "Dados de escolas não disponíveis"
            
            # Calcular distâncias
            escolas_com_distancia = []
            
            for _, escola in self.escolas_df.iterrows():
                distancia = self.calcular_distancia(
                    lat_cep, lng_cep,
                    escola['Latitude'], escola['Longitude']
                )
                
                escola_info = {
                    'nome': escola['Escola'],
                    'codigo_inep': escola['Codigo_INEP'],
                    'endereco': escola['Endereco'],
                    'municipio': escola['Municipio'],
                    'uf': escola['UF'],
                    'distancia_km': round(distancia, 2),
                    'telefone': '(11) 3456-7890'  # Telefone genérico
                }
                
                escolas_com_distancia.append(escola_info)
            
            # Ordenar por distância e pegar as mais próximas
            escolas_ordenadas = sorted(escolas_com_distancia, key=lambda x: x['distancia_km'])
            escolas_proximas = escolas_ordenadas[:limite]
            
            # Formatizar resultado
            resultado = {
                'cep_info': dados_cep,
                'escolas': []
            }
            
            for escola in escolas_proximas:
                resultado['escolas'].append({
                    'nome': escola['nome'],
                    'endereco': escola['endereco'],
                    'municipio': escola['municipio'],
                    'uf': escola['uf'],
                    'distancia': f"{escola['distancia_km']} km",
                    'telefone': escola['telefone'],
                    'codigo_inep': escola['codigo_inep']
                })
            
            return resultado, None
            
        except Exception as e:
            logging.error(f"Erro ao buscar escolas próximas: {e}")
            return None, f"Erro interno: {str(e)}"

# Instância global do serviço
escola_service = EscolaService()