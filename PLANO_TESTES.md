# Plano de Testes Funcionais — Migração Odoo (pós-migração, "teste profundo")

Este documento descreve a metodologia de teste automático implementada em
`quality_test.js` (Playwright + Node.js), usada para validar uma base de dados
Odoo depois de uma migração de versão. Serve de exemplo/modelo para construir
um plano semelhante noutro contexto.

## Objetivo

Confirmar que, depois de uma migração, **cada ecrã real que um utilizador
usaria** continua a abrir, a mostrar dados e a permitir criar um registo novo
— sem erros de JavaScript, sem pedidos ao servidor a falhar, sem exceções por
apanhar. O objetivo não é testar regras de negócio (isso é para testes
unitários do Odoo), é apanhar **regressões de migração**: campos que
deixaram de existir, vistas partidas, menus órfãos, módulos desativados que
ainda são referenciados, etc.

## Âmbito (o que é testado)

Uma lista fixa de **apps** (`APPS`, ~32 apps: Contactos, CRM, Vendas,
Contabilidade, Projeto, Inventário, Funcionários, Assiduidades, etc.) —
alinhada com o que o cliente concreto tem instalado.

Para cada app, o script:

1. Abre a app a partir da página inicial (`/odoo`).
2. Testa a **vista raiz** da app (o ecrã que abre por omissão).
3. Descobre dinamicamente as **secções do menu de topo** dessa app
   (`.o_menu_sections`) — não é uma lista escrita à mão, é lida da própria
   interface, por isso cobre automaticamente o que a app realmente tem.
4. Para cada secção:
   - Se for um **dropdown** (grupo com vários itens), testa cada item
     individualmente.
   - Se for um **ecrã direto**, testa esse ecrã.

Por cada ecrã ("leaf"), dois testes:

- **Abrir um registo existente**: se houver dados na lista/kanban, abre o
  primeiro registo, percorre até 6 separadores do formulário, volta à lista.
- **Criar um registo novo**: clica em "Novo", preenche os campos obrigatórios
  visíveis com dados de teste genéricos (texto, data de hoje, primeira opção
  de selects, primeiro resultado de autocomplete em many2one/many2many),
  tenta guardar.

### Exceção deliberada — apps só de configuração

`VIEW_ONLY_APPS = ['Definições', 'Apps', 'Testes']` — nestas apps só se testa
**abrir**, nunca criar. É risco desnecessário criar registos em ecrãs de
configuração viva do sistema (ex.: parâmetros gerais, lista de módulos).

## Critério de falha real vs. ruído (muito importante)

Um item só conta como **problema real** se acontecer pelo menos um destes,
durante a navegação a esse ecrã específico:

- `recordStatus` ou `createStatus` começar por `error:` ou `navigation error:`
  (uma ação de Playwright rebentou — clique, preenchimento, navegação).
- Houve pelo menos um erro real de consola (`console.error`), erro de página
  (`pageerror`) ou pedido HTTP ≥400, **depois de filtrar ruído conhecido**.

Ruído conhecido, sempre ignorado (não conta como falha):

- Qualquer erro relacionado com imagens em falta (extensão de imagem,
  `/web/image/...`, `image_128`/`image_256`/etc., previews de PDF/anexos) —
  filestore incompleto é um problema à parte, não uma regressão de código.
- A mensagem genérica do browser `Failed to load resource: ...` sem URL —
  é sempre redundante com o `failedRequests` correspondente, que já tem o
  URL e fica capturado à parte.

Isto é decidido por `isImageNoise()`/`isGenericResourceNotice()` em
`quality_test.js` — mantém a taxa de falsos positivos baixa sem esconder
problemas genuínos.

### Falsos positivos que NÃO são deste tipo de ruído (lição aprendida)

Nem todo o "erro" reportado pelo script é um bug da aplicação. Confirmado em
2026-08-24 (migração admincore): alguns "nav error" foram investigados à mão
(reprodução manual com browser real, fora do script) e eram **limitações do
próprio script de teste** — ex.: à procura de uma barra `.o_menu_sections`
que uma app específica não usa naquele layout. **Sempre que um "problema"
parecer estranho ou isolado, vale a pena reproduzir manualmente antes de
"corrigir" código da aplicação** — o script é uma boa primeira passagem, não
a palavra final.

## Como correr

```
node quality_test.js <job_id> [base_url] [app_name_opcional]
```

- `job_id`: identifica a run (nome da pasta de resultados).
- `base_url`: por omissão `http://10.10.10.88:8019`.
- `app_name_opcional`: para testar só uma app durante debug, em vez da lista toda.

Autenticação: usa um cookie de sessão já válido (`session_id`), passado via
variável de ambiente `PANEL_SESSION_ID` (o painel trata disto automaticamente
ao clicar em "Criar teste de qualidade" — repõe passwords de teste e
autentica antes de lançar o script). Não faz login por formulário.

## Saídas (por cada run, em `static/test-results/<job_id>/`)

- **`video.webm`** — gravação de todo o browser durante o teste (1280×800).
  Cada erro no log inclui o intervalo de tempo no vídeo (`[mm:ss–mm:ss]`)
  onde aconteceu, para ir direto ao momento certo em vez de ver tudo.
- **`log.txt`** — relatório legível em PT-PT: um resumo (duração, quantos
  itens testados, quantos com problemas), depois cada item OK numa linha, e
  cada problema com o passo-a-passo até ao erro e as mensagens reais.
- **`results.json`** — os mesmos dados em bruto, estruturados, para
  consumo programático (é o que o painel lê para desenhar a UI de
  resultados).

## Duração e escala

Um teste profundo cobre tipicamente 250-300 combinações app+ecrã e demora
1-2 horas (a maior parte do tempo é `waitForTimeout` deliberado entre ações,
para dar tempo à interface renderizar sem falsos negativos por pressa).

## Ideias para adaptar este plano a outro contexto

- A lista `APPS` deve refletir o que o cliente concreto tem instalado — não
  copiar cegamente.
- O padrão "abrir root → descobrir secções na própria UI → dropdown vs. ecrã
  direto → abrir registo + criar registo" generaliza bem a qualquer app
  Odoo baseada em `ir.ui.menu`/`ir.actions.act_window`.
- Vale sempre a pena ter uma lista de "ruído conhecido" explícita e um
  critério de falha central (`hasRealProblem()`) — evita alarme falso em
  cada run e mantém o histórico de resultados comparável ao longo do tempo.
- Gravar vídeo com timestamp por erro poupa imenso tempo a diagnosticar
  depois, comparado com só texto de erro.

---

# Lacuna identificada (2026-08-24, migração admincore v19)

## O que o `quality_test.js` NÃO testa

O script cria um registo e clica em **"Guardar"** — e pára aí
(`quality_test.js:285`, único ponto onde há clique de ação). Nunca:

- **adiciona linhas** ao documento (um orçamento fica sem artigos)
- **confirma** (o orçamento fica em rascunho, nunca chega a Ordem de Venda)
- **envia email** ao cliente
- **fatura / lança / paga**
- **valida receções** no inventário

Isto aplica-se a **todos** os módulos, não só às Vendas. Um "OK" do script quer dizer
*"o formulário abre e grava um rascunho"* — não que o processo de negócio funcione.

### Porque é que isso importa

Nesta migração, o varrimento de vistas deu **504 OK em 545 ações de menu** e, ao mesmo
tempo, **não era possível emitir uma fatura**. Vistas OK != aplicação funcional. O bug
(contas do plano sem empresa) só apareceu ao correr o fluxo completo.

## Complemento recomendado: teste de fluxos de negócio

Correr, além do `quality_test.js`, um script Python no `odoo-bin shell` que exercite os
fluxos ponta-a-ponta. Cada fluxo dentro de um **savepoint revertido no fim**, para não
deixar lixo na BD:

```python
def step(nome, fn):
    cr.execute("SAVEPOINT f")
    try:
        det = fn() or ""
        R.append(("OK", nome, det))
    except Exception as ex:
        R.append(("FALHA", nome, f"{type(ex).__name__}: {str(ex)[:180]}"))
    cr.execute("ROLLBACK TO SAVEPOINT f")
    env.invalidate_all()          # obrigatório: a cache do ORM fica suja após o rollback
```

**Savepoints não são opcional:** sem eles o primeiro erro SQL aborta a transação
(`InFailedSqlTransaction`) e tudo o que vem a seguir falha em cascata, escondendo os
resultados verdadeiros.

### Fluxos a cobrir (mínimo)

| Módulo | Fluxo |
|---|---|
| Vendas | orçamento **com linhas** -> confirmar -> enviar email -> faturar -> lançar |
| Compras | encomenda **com linhas** -> confirmar -> receber mercadoria |
| Faturação | fatura -> lançar -> registar pagamento -> nota de crédito |
| Inventário | transferência -> validar |
| RH | ausência -> aprovar |

### Emails: o que dá para testar numa BD neutralizada

Numa BD neutralizada não sai email real (é esse o objetivo). Testável na mesma:

```python
# 1) o template renderiza? (apanha campos removidos/renomeados no corpo do email)
tpl = env.ref('sale.email_template_edi_sale')
body = tpl._render_field('body_html', so.ids)[so.id]
subj = tpl._render_field('subject', so.ids)[so.id]

# 2) o envio ao cliente cria a mensagem?
msg = so.message_post(body="...", partner_ids=[cliente.id],
                      message_type='comment', subtype_xmlid='mail.mt_comment')
```

Renderizar o template é o que apanha regressões de migração (um campo que desapareceu
rebenta o QWeb do email). O envio SMTP em si não é testável nem desejável aqui.

## Escolher dados de teste válidos (senão o teste mente)

Os primeiros resultados foram falsos negativos por **dados de teste maus**, não por bugs:

- `ValidationError: Deve existir um e apenas um imposto de IVA por linha`
  -> o artigo apanhado pelo `search(limit=1)` tinha 0 ou 2 impostos.
  **Escolher um artigo com exactamente 1 imposto da empresa em teste.**
- `UserError: É necessário definir um local de fornecedor`
  -> fornecedor sem localização configurada.
  **Usar um parceiro que já apareça em encomendas reais confirmadas.**

```python
# artigo com exactamente 1 imposto de venda da empresa
[p for p in Produtos.search([('sale_ok','=',True)], limit=400)
   if len(p.taxes_id.filtered(lambda t: t.company_id == empresa)) == 1]

# fornecedor comprovadamente utilizável
env['purchase.order'].search([('state','in',('purchase','done'))], limit=1).partner_id
```

## Certificação PT: falha esperada, NÃO é bug

Em BD neutralizada, confirmar uma venda pode dar:

```
UserError: Comunicação com Webservice não é suportada no modo de Teste.
  at_webservice_mixin.at_ws_communication
```

É a certificação a **proteger-se**: confirmar o documento pede o ATCUD à AT, e o módulo
bloqueia a comunicação a partir de uma cópia de teste. **É o comportamento correto** — não
deve ser "corrigido". Ao classificar resultados, tratar como *esperado* e testar o resto
do fluxo (email, faturação de documentos já existentes) à volta dele.

## Correr o `quality_test.js` fora do servidor do painel

```bash
mkdir -p ~/odoo19/qtest && cd ~/odoo19/qtest
npm init -y && npm install playwright-core
npx playwright install chromium
cp ../quality_test.js .
# adaptar: RESULTS_ROOT -> ./test-results ; BASE -> http://localhost:8017
# a sessão é lida de /tmp/pw-smoke/session_id.txt (ou env PANEL_SESSION_ID);
# obter por RPC a /web/session/authenticate — o script não faz login por formulário
node quality_test.js <job_id> http://localhost:8017 ["App"]   # App opcional, p/ debug
```

---

# Inspecionar a UI, não confiar só no automatismo

O `quality_test.js` corre **cego**: reporta `create=ok` (gravou um rascunho) ou
`create=no "new" button found`, sem distinguir **"o botão não existe"** de
**"o botão está escondido por uma condição `invisible`"**. São coisas muito diferentes.

## Caso real (admincore v19, 2026-08-24)

Ao inspecionar um orçamento novo no browser, a barra de botões era:

```
Enviar | Imprimir | Pré-visualizar | Publicar        <-- não há "Confirmar"
```

O `quality_test.js` teria dito apenas "guardado, OK". Só a inspeção revelou que o fluxo
de vendas nesta instalação é **draft -> Publicar -> Confirmar** (imposto pela certificação
PT/AO), e não o `draft -> Confirmar` do Odoo standard.

**Consequência:** um teste de fluxos que faça `create()` -> `action_confirm()` está a
testar um caminho que **na interface não existe**. Testar sempre pela ordem que a UI impõe.

## Como inspecionar (Claude-in-Chrome ou consola do browser)

```javascript
// que botões existem na statusbar, e quais estão realmente visíveis?
[...document.querySelectorAll('.o_statusbar_buttons button')].map(b => ({
  texto: b.innerText.trim(),
  name:  b.getAttribute('name'),
  visivel: b.offsetParent !== null,      // false = escondido por CSS/invisible
  disabled: b.disabled,
}));
```

```javascript
// o botão existe no arch mas está escondido? ver a condição 'invisible'
const j = await (await fetch('/web/dataset/call_kw', {method:'POST',
  headers:{'Content-Type':'application/json'},
  body: JSON.stringify({jsonrpc:"2.0", method:"call", params:{
    model:'sale.order', method:'get_views',
    args:[[[false,'form']]], kwargs:{options:{}}}})})).json();
[...j.result.views.form.arch.matchAll(/<button[^>]*name="([^"]+)"[^>]*>/g)]
  .map(m => m[0]).filter(b => b.includes('action_confirm'));
// -> <button name="action_confirm" ... invisible="state != 'sent'"/>
```

Distinguir os três casos:
1. **não está no arch** -> o módulo que o define não está instalado, ou uma vista removeu-o
2. **está no arch com `invisible=...`** -> comportamento intencional; perceber a condição
3. **está no arch, sem `invisible`, mas `offsetParent === null`** -> aí sim, provável bug de CSS/layout

## Nota sobre carga da máquina

Correr o `quality_test.js` e inspeção manual no browser **ao mesmo tempo** satura a
máquina (load > 4) e o browser começa a falhar a renderizar formulários — dando falsos
"ecrã em branco". Nesse estado, validar por **RPC** (`/web/dataset/call_kw`), que não
depende de renderização, e deixar a inspeção visual para quando a run terminar.
