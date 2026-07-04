# ADS Client - Relatório PySpark de Pedidos

Projeto final de Data Engineering Programming para gerar um relatório de pedidos de venda de 2025 cujos pagamentos foram recusados (`status=false`) e cuja avaliação de fraude classificou o pedido como legítimo (`avaliacao_fraude.fraude=false`).

Link público do repositório Github para inserir no PDF de entrega:
https://github.com/SEU-USUARIO/ads-client

## Saída esperada

O pipeline grava o relatório em Parquet no caminho:

```text
data/output/relatorio_pedidos_2025_parquet
```

A saída contém:

1. `id_pedido`
2. `uf`
3. `forma_pagamento`
4. `valor_total_pedido` (calculado como `VALOR_UNITARIO * QUANTIDADE` do pedido)
5. `data_pedido`

A ordenação é por `uf`, `forma_pagamento` e `data_pedido`.

## Estrutura do projeto

```text
src/
  main.py
  ads_client/
    config/
    spark/
    io/
    schemas/
    business/
    pipeline/
tests/
data/
  input/
  output/
```

## Como executar

Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
pip install -e .
```

Garanta que os datasets existam nos caminhos abaixo:

```text
data/input/datasets-csv-pedidos-main/data/pedidos/
data/input/dataset-json-pagamentos-main/data/pagamentos/
```

Execute o pipeline:

```bash
python src/main.py
```

## Como validar o resultado

Exemplo para inspecionar o Parquet gerado:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[*]").appName("validacao").getOrCreate()
df = spark.read.parquet("data/output/relatorio_pedidos_2025_parquet")
df.show(20, truncate=False)
df.printSchema()
spark.stop()
```

## Como executar testes unitários

```bash
pytest -q
```

## Decisões técnicas

- Todos os DataFrames são lidos com schemas explícitos.
- Todos os componentes foram encapsulados em classes.
- `src/main.py` atua como Aggregation Root.
- As dependências são instanciadas no fluxo principal e injetadas no pipeline.
- Há pacotes dedicados para configuração, sessão Spark, I/O, lógica de negócio e orquestração.
- A classe `SalesReportService` importa, configura e utiliza `logging`.
- A lógica de negócio usa `try/except` para registrar e relançar erros.
