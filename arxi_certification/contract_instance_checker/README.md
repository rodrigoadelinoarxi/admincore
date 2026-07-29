# Contract Instance Checker

**Version:** 18.0.1.0.0
**Author:** FlyByOdoo
**License:** LGPL-3

## Descrição

Módulo para instalação em instâncias controladas (Odoo 17 ou 18) que valida automaticamente o contrato com o sistema central FlyByOdoo.

Este módulo garante que apenas instâncias com contratos válidos podem ser utilizadas, implementando um sistema de segurança robusto e difícil de adulterar.

## Características

### Validação Automática

- **Cron Job Diário:** Valida o contrato com o servidor central automaticamente
- **Cache de Status:** Armazena o último estado de validação para referência
- **Histórico:** Mantém registo de todas as validações realizadas

### Alertas Visuais

O sistema exibe alertas claros no topo da interface quando:
- O contrato está próximo da expiração (menos de 30 dias)
- O número de utilizadores excede o limite contratado
- O contrato expirou
- Há erro na validação com o servidor central

### Bloqueio de Instância

Quando o contrato expira e `block_instance=True`:
- Nenhum utilizador consegue fazer login (exceto superuser)
- Mensagem clara de erro é apresentada
- Acesso bloqueado ao nível de autenticação (não pode ser contornado via interface)

### Configuração Simples

Configure apenas três parâmetros em Settings:
1. **NIF:** Número de Identificação Fiscal
2. **Token:** Token de acesso fornecido pelo sistema central
3. **URL do Servidor Central:** URL do sistema FlyByOdoo central

## Instalação

1. Copie o módulo para a pasta de addons da instância controlada
2. Atualize a lista de módulos
3. Instale o módulo "Contract Instance Checker"
4. Configure os parâmetros em Settings

## Configuração

### Passo 1: Obter Credenciais

Contacte o suporte FlyByOdoo para obter:
- NIF da sua empresa
- Token de acesso único
- URL do servidor central (normalmente: `https://central.flybyodoo.com`)

### Passo 2: Configurar Instância

1. Aceda a **Settings > Contract Instance Checker**
2. Preencha:
   - **Instance NIF:** Seu NIF
   - **Instance Token:** Token fornecido pela FlyByOdoo
   - **Central Server URL:** URL do servidor central
3. Clique em **Save**
4. Clique em **Validate Now** para testar a conexão

### Passo 3: Verificar Status

Após validar, verifique:
- **Contract Status:** Deve mostrar "Active"
- **End Date:** Data de fim do seu contrato
- **User Limit:** Número máximo de utilizadores
- **Days Until Expiration:** Dias restantes

## Utilização

### Dashboard de Status

Na página de Settings > Contract Instance Checker, pode ver:

#### Status Ativo (Verde)
```
✓ Contract Active
Your contract is active and valid.
• End Date: 2025-12-31
• Days Remaining: 365
• Users: 12 / 20
```

#### Alerta de Expiração (Amarelo)
```
⚠ Warning: Contract Expiring Soon!
Your contract will expire in 25 days.
Please contact FlyByOdoo support to renew your contract.
```

#### Alerta de Limite de Utilizadores (Amarelo)
```
⚠ Warning: User Limit Exceeded!
Current users (22) exceeds the limit (20).
Please contact FlyByOdoo support to increase your user limit.
```

#### Contrato Expirado (Vermelho)
```
✗ Contract Expired or Not Found!
Your contract is no longer valid. Access may be blocked.
Please contact FlyByOdoo support immediately.
```

### Validação Manual

Pode forçar uma validação imediata a qualquer momento:
1. Aceda a Settings > Contract Instance Checker
2. Clique no botão **Validate Now**
3. A página irá recarregar com o status atualizado

### Validação Automática

O sistema executa automaticamente uma validação diária:
- **Horário:** Configurável via cron job
- **Ação:** Consulta o servidor central via API
- **Dados Enviados:** NIF, Token, Contagem de utilizadores
- **Resultado:** Atualiza o status local do contrato

## Segurança

### Sistema de Bloqueio

O bloqueio de instância é implementado ao nível da autenticação:
- Intercepta o método `_check_credentials` do modelo `res.users`
- Verifica o status do contrato antes de permitir login
- Não pode ser contornado via interface ou manipulação de dados
- Exceções apenas para utilizadores de sistema (admin, root)

### Proteção contra Adulteração

O sistema é difícil de adulterar porque:
- Validação acontece no código Python (não apenas JavaScript)
- Bloqueio ao nível de autenticação
- Token armazenado de forma segura
- Validação com servidor externo (não local)
- Logs de todas as operações

### Permissões

- **Utilizadores normais:** Apenas leitura do status
- **Administradores (System):** Configuração e gestão completa

## API de Comunicação

O módulo comunica com o servidor central via API REST.

### Endpoint Utilizado

```
GET /api/contract/check
```

### Parâmetros Enviados

```json
{
  "nif": "123456789",
  "token": "unique_token_here",
  "user_count": 12
}
```

### Resposta Esperada (Sucesso)

```json
{
  "status": "active",
  "end_date": "2025-12-31",
  "user_limit": 20,
  "block_instance": true,
  "contract_name": "Contrato Cliente ABC",
  "contract_type": "flybyodoo",
  "days_until_expiration": 365
}
```

### Resposta Esperada (Erro)

```json
{
  "error": "No active contract found",
  "error_code": "CONTRACT_NOT_FOUND"
}
```

## Modelos de Dados

### contract.instance.status

Armazena o histórico e cache das validações:

**Campos principais:**
- `last_check_date`: Data/hora da última verificação
- `contract_status`: Estado do contrato (active, expired, error, not_found)
- `end_date`: Data de fim do contrato
- `user_limit`: Limite de utilizadores
- `current_user_count`: Contagem atual de utilizadores
- `block_instance`: Se deve bloquear quando expirado
- `days_until_expiration`: Dias restantes
- `error_message`: Mensagem de erro (se houver)

**Campos computados:**
- `is_expiring_soon`: True se faltar menos de 30 dias
- `is_user_limit_exceeded`: True se utilizadores > limite
- `is_instance_blocked`: True se deve estar bloqueado

## Cron Jobs

### Validação Diária

- **Nome:** Instance Checker: Validate Contract Daily
- **Modelo:** contract.instance.status
- **Método:** `_cron_validate_contract()`
- **Frequência:** Diária
- **Prioridade:** 5 (alta)

## Dependências

- base
- web

## Estrutura de Ficheiros

```
contract_instance_checker/
├── __init__.py
├── __manifest__.py
├── data/
│   └── instance_checker_cron.xml
├── models/
│   ├── __init__.py
│   ├── contract_instance_status.py
│   ├── res_config_settings.py
│   └── res_users.py
├── security/
│   └── ir.model.access.csv
├── static/
│   └── src/
│       └── scss/
│           └── contract_alert.scss
├── views/
│   ├── contract_status_templates.xml
│   └── res_config_settings_views.xml
└── README.md
```

## Fluxo de Funcionamento

### 1. Instalação e Configuração
```
Instalar módulo → Configurar NIF, Token, URL → Validar manualmente
```

### 2. Validação Diária Automática
```
Cron executa → Conta utilizadores → Consulta API central →
Recebe resposta → Cria registo status → Atualiza cache
```

### 3. Verificação ao Login
```
Utilizador tenta login → Valida password → Verifica contract status →
Se bloqueado: AccessDenied → Se OK: Login permitido
```

### 4. Alertas na Interface
```
Utilizador logado → Sistema verifica status → Se alerta necessário:
Exibe banner no topo → Utilizador vê aviso
```

## Troubleshooting

### Erro: "Unable to validate contract"

**Causas possíveis:**
- URL do servidor central incorreto
- Servidor central inacessível
- Problema de rede/firewall

**Solução:**
1. Verifique a URL em Settings
2. Teste conectividade: `curl https://central.flybyodoo.com/api/contract/health`
3. Verifique firewall/proxy
4. Contacte suporte FlyByOdoo

### Erro: "No active contract found"

**Causas possíveis:**
- NIF ou Token incorretos
- Contrato não existe no servidor central
- Contrato não está ativo

**Solução:**
1. Verifique NIF e Token em Settings
2. Contacte suporte FlyByOdoo para verificar contrato
3. Valide se contrato está ativo no sistema central

### Não consigo fazer login

**Causas possíveis:**
- Contrato expirado e block_instance=True
- Erro na última validação

**Solução:**
1. Contacte suporte FlyByOdoo urgentemente
2. Se for superuser (admin), consegue aceder para verificar
3. Verifique logs do Odoo para detalhes do bloqueio

### Alertas não aparecem

**Causas possíveis:**
- CSS não carregado
- Validação não executou
- Status não atualizado

**Solução:**
1. Faça validação manual em Settings
2. Limpe cache do browser
3. Atualize assets do Odoo: `odoo-bin -u contract_instance_checker`

## Mensagens de Erro

### AccessDenied: Contract Expired

```
Your FlyByOdoo contract has expired on 2025-01-01.
Please contact FlyByOdoo support to renew your contract.
```

**Ação:** Contacte suporte para renovar contrato

### AccessDenied: No Valid Contract

```
No valid contract found for this instance.
Please contact FlyByOdoo support.
```

**Ação:** Verifique configuração NIF/Token ou contacte suporte

### AccessDenied: Validation Error

```
Unable to validate contract: Connection timeout.
Please contact FlyByOdoo support.
```

**Ação:** Verifique conectividade e configuração

## Boas Práticas

### Para Administradores

1. **Configure alertas:** Mantenha o email do administrador atualizado
2. **Monitore regularmente:** Verifique o status semanalmente
3. **Renove antecipadamente:** Não espere pelo último dia
4. **Teste após instalação:** Execute validação manual após configurar
5. **Mantenha credenciais seguras:** Não partilhe NIF/Token

### Para Utilizadores

1. **Atente aos alertas:** Não ignore avisos de expiração
2. **Reporte problemas:** Informe administrador se vir alertas
3. **Não tente contornar:** O sistema de bloqueio é à prova de adulteração

## Suporte

Para questões, problemas ou renovação de contrato:

**Contacto FlyByOdoo Support**
- Email: support@flybyodoo.com
- Telefone: +351 XXX XXX XXX
- Website: https://www.flybyodoo.com

## Changelog

### Version 18.0.1.0.0
- Release inicial para Odoo 18.0
- Sistema de validação automática com servidor central
- Bloqueio de instância quando contrato expira
- Alertas visuais no topo da interface
- Dashboard de status em Settings
- Histórico de validações
- Sistema de segurança robusto
