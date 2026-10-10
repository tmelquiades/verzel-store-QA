# Verzel Store · Automação de testes (Playwright + Python)

Automação de 3 casos de teste da funcionalidade **VZS-142 · Cupom de desconto e frete grátis** (v2.3.0), em `https://verzel-store.qa-test-verzel-store.workers.dev`.

## CTs automatizados

| CT | Arquivo | Critério | Resultado esperado da execução |
|---|---|---|---|
| UI-01 · Finalizar compra sem etapa de pagamento online | `tests/test_UI_01_finalizar_compra.py` | Regras pré-existentes (pagamento na entrega) | **Passa** |
| QTD-07 · Limite de 5 unidades na interface | `tests/test_QTD_07_limite_de_5.py` | CA10 | **Passa** |
| FRT-03 · Limite exato: subtotal R$ 200,00 tem frete grátis | `tests/test_FRT_03_limite_exato.py` | CA06 | **Falha** (reproduz o **BUG-01**) |

> O FRT-03 está marcado com `@pytest.mark.bug`. Ele deve falhar enquanto o BUG-01 não for corrigido: o carrinho cobra frete de R$ 19,90 e exibe "Faltam R$ 0,00 para o frete grátis." em vez de aplicar o frete grátis. Depois da correção, a marca `bug` deve ser removida e o teste deve passar.

Resultado esperado de `pytest`: **2 passed, 1 failed**.

## Pré-requisitos

- Python 3.9 ou superior
- Acesso à internet (o ambiente da Verzel Store é público)

## Estrutura

```
verzel-store-automacao/
├── README.md
├── requirements.txt          # dependências
├── pytest.ini                # base_url, evidências automáticas e marcas
├── conftest.py               # classe Loja (ações reutilizáveis) e fixture "loja"
└── tests/
    ├── test_FRT_03_limite_exato.py
    ├── test_QTD_07_limite_de_5.py
    └── test_UI_01_finalizar_compra.py
└── docs/
    ├── casos_de_teste_verzel_store.pdf
    ├── evidencias_execucao_verzel_store.pdf
    └── relatorio_de_bugs_verzel_store.pdf
```

## Instalação

Na pasta do projeto:

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Como executar

| Objetivo | Comando |
|---|---|
| Rodar todos os testes | `pytest` |
| Ver o navegador abrindo | `pytest --headed` |
| Ver mais devagar (500 ms por ação) | `pytest --headed --slowmo 500` |
| Rodar um teste | `pytest tests/test_UI_01_finalizar_compra.py` |
| Rodar só os que devem passar | `pytest -m "not bug"` |
| Rodar só o CT que reproduz o bug | `pytest -m bug` |
| Gerar relatório HTML | `pytest --html=reports/relatorio.html --self-contained-html` |

## Evidências em caso de falha

O `pytest.ini` já configura a coleta automática de evidências **apenas para testes que falham**. Elas ficam na pasta `test-results/`:

- screenshot da tela no momento da falha
- vídeo da execução
- trace do Playwright (`trace.zip`)

Para abrir o trace, com linha do tempo, DOM e rede de cada passo:

```bash
playwright show-trace test-results/<pasta-do-teste>/trace.zip
```

## Decisões de projeto

- **Isolamento:** o carrinho da loja fica guardado só na aba do navegador. Como o pytest-playwright abre um contexto novo para cada teste, cada teste começa com o carrinho vazio e não depende dos outros.
- **URL base:** definida em `pytest.ini`. Para testar outro ambiente, use `pytest --base-url https://outro-ambiente`.
- **Reuso:** a classe `Loja` (em `conftest.py`) concentra as ações repetidas (adicionar produto, abrir carrinho, aumentar quantidade). Os testes ficam curtos e seguem o formato Dado / Quando / Então.
- **Localizadores:** priorizam papéis e nomes acessíveis (`get_by_role`). Os valores do resumo do pedido usam o atributo `data-valor` (`subtotal`, `desconto`, `frete` e `total`).

## Solução de problemas

| Sintoma | O que fazer |
|---|---|
| `pytest` ou `playwright` não é reconhecido | Ative o ambiente virtual ou use `python -m pytest` e `python -m playwright install chromium` |
| PowerShell bloqueia o `Activate.ps1` | Execute `Set-ExecutionPolicy -Scope Process RemoteSigned` e ative de novo |
| Erro de navegador não instalado | Rode `playwright install chromium` |
| Teste falha por `data-valor='subtotal'` (ou `total`) não encontrado | Confira o atributo real no DOM com `playwright codegen https://verzel-store.qa-test-verzel-store.workers.dev` (ou o DevTools) e ajuste o método `valor()` em `conftest.py` |
| `strict mode violation` | O localizador encontrou mais de um elemento. Torne-o mais específico ou use `.first` |

## Observações

A Verzel Store é um ambiente fictício de teste técnico: nenhuma compra é real e nada é armazenado entre execuções.
