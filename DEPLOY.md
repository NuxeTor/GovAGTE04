# Deploy no Heroku - IBGE Trabalhe Conosco

## Arquivos Configurados para Deploy

### 1. Aplicação Principal
- `app_simple.py` - Aplicação Flask simplificada sem dependências complexas
- `nova_era_api.py` - Integração PIX Nova Era com credenciais reais
- `templates/` - Templates HTML com design gov.br oficial

### 2. Configuração Heroku
- `Procfile` - Configuração Gunicorn otimizada
- `requirements.txt` - Dependências mínimas (Flask, gunicorn, requests)
- `runtime.txt` - Python 3.11.10
- `app.json` - Deploy automático com variáveis configuradas

### 3. Credenciais Configuradas
- **NOVA_ERA_SECRET_KEY**: `sk_uluAT1O9I6FGTQAcXzccr2H_eAQ9IOzYoY_LLDfR8U6Uv2Xb`
- **NOVA_ERA_PUBLIC_KEY**: `pk_E5SWGB_rZ-mZowMITdSr5w8zhOdY8TDImLhOM-s9gmJPoc9x`
- **SESSION_SECRET**: Gerado automaticamente pelo Heroku

## Deploy Automático

### Opção 1: Deploy Button
Clique no botão de deploy automático no README ou use:
```
https://heroku.com/deploy?template=https://github.com/user/repo
```

### Opção 2: Heroku CLI
```bash
# 1. Login no Heroku
heroku login

# 2. Criar app
heroku create ibge-trabalhe-conosco

# 3. Configurar variáveis
heroku config:set SESSION_SECRET=$(openssl rand -base64 32)
heroku config:set NOVA_ERA_SECRET_KEY=sk_uluAT1O9I6FGTQAcXzccr2H_eAQ9IOzYoY_LLDfR8U6Uv2Xb
heroku config:set NOVA_ERA_PUBLIC_KEY=pk_E5SWGB_rZ-mZowMITdSr5w8zhOdY8TDImLhOM-s9gmJPoc9x

# 4. Deploy
git push heroku main
```

## Funcionalidades Testadas
- ✅ Página inicial do IBGE
- ✅ Validação CPF via API externa
- ✅ Geração PIX Nova Era (transações reais)
- ✅ Comprovante oficial com brasão da República
- ✅ Popup gov.br com proteção LGPD
- ✅ Fluxo completo: formulário → comprovante → PIX

## URLs da Aplicação
- **Produção**: `https://[app-name].herokuapp.com`
- **Desenvolvimento**: `http://localhost:5000`

## Monitoramento
- Logs: `heroku logs --tail`
- Status: `heroku ps`
- Métricas: Dashboard Heroku

## Resolução de Problemas
1. **App não abre**: Verificar logs com `heroku logs --tail`
2. **Erro 500**: Verificar variáveis de ambiente configuradas
3. **PIX não funciona**: Verificar credenciais Nova Era no config vars
4. **Timeout**: App está configurado com timeout de 30s