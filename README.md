# Otimizador de Builds Fictícias com FastAPI

Aplicação demonstrativa que compara combinações de equipamentos inventados e explica como ataque, afinidade, elemento, defesa e habilidades influenciam uma pontuação.

> Todos os nomes, atributos e alvos deste repositório são fictícios. O projeto não utiliza marcas, imagens, ícones ou bases de dados de jogos comerciais.

## Funcionalidades

- catálogo JSON com equipamentos e criaturas fictícias;
- avaliação de uma combinação escolhida;
- busca exaustiva da melhor combinação disponível;
- decomposição explicável do cálculo;
- API documentada automaticamente pelo FastAPI;
- interface web responsiva sem dependências externas;
- testes do motor e dos endpoints.

## Tecnologias

- Python 3.12+
- FastAPI e Pydantic
- HTML, CSS e JavaScript
- Pytest e HTTPX
- Docker opcional

## Instalação local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

## Execução

```powershell
python -m uvicorn app.main:app --reload
```

Acesse:

- interface: `http://127.0.0.1:8000/`;
- documentação da API: `http://127.0.0.1:8000/docs`;
- diagnóstico: `http://127.0.0.1:8000/api/health`.

## Docker

```powershell
docker compose up --build
```

## Testes

```powershell
python -m pytest -q
```

## Como funciona o cálculo

O motor calcula dano físico e elemental separadamente. A afinidade altera o dano físico esperado, habilidades aplicam bônus limitados e as resistências do alvo reduzem cada parcela. A pontuação final soma o dano estimado a 20% da defesa total.

O algoritmo de otimização avalia todas as armas e uma opção de armadura para cada slot. O catálogo é pequeno por intenção, permitindo demonstrar busca exaustiva sem apresentar os números como balanceamento real.

## Estrutura

```text
app/      API, modelos, carregamento e motor
data/     catálogo exclusivamente fictício
static/   interface web sem ativos de terceiros
tests/    testes automatizados
```

## Limitações

- a fórmula é didática e não representa um jogo real;
- a busca exaustiva não é indicada para catálogos muito grandes;
- não há autenticação nem persistência de builds;
- implantação em produção exige configuração adicional de segurança e observabilidade.

## Resultados

| Indicador | Resultado |
|---|---|
| Tempo de resposta | [PREENCHER] |
| Combinações avaliadas | [PREENCHER] |
| Cobertura de testes | [PREENCHER] |

## Licença

MIT. Consulte `LICENSE`.
