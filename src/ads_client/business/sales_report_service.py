import logging

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class SalesReportService:
    """Aplica a lógica de negócio do relatório de pedidos solicitado."""

    def build_report(self, pedidos_df: DataFrame, pagamentos_df: DataFrame, year: int) -> DataFrame:
        try:
            logging.info("Iniciando construção do relatório de pedidos do ano %s.", year)

            logging.info("Filtrando pedidos pelo ano de criação.")
            pedidos_ano_df = (
                pedidos_df.withColumn("data_pedido", F.to_timestamp(F.col("DATA_CRIACAO")))
                .filter(F.year(F.col("data_pedido")) == year)
                .withColumn(
                    "valor_total_pedido",
                    F.col("VALOR_UNITARIO") * F.col("QUANTIDADE"),
                )
                .select(
                    F.col("ID_PEDIDO").alias("id_pedido"),
                    F.col("UF").alias("uf"),
                    F.col("valor_total_pedido"),
                    F.col("data_pedido"),
                )
            )

            logging.info("Filtrando pagamentos recusados e classificados como legítimos.")
            pagamentos_legitimos_recusados_df = pagamentos_df.filter(
                (F.col("status") == F.lit(False))
                & (F.col("avaliacao_fraude.fraude") == F.lit(False))
            ).select(
                F.col("id_pedido"),
                F.col("forma_pagamento"),
            )

            logging.info("Unindo pedidos e pagamentos, selecionando atributos e ordenando.")
            relatorio_df = (
                pedidos_ano_df.join(pagamentos_legitimos_recusados_df, "id_pedido", "inner")
                .select(
                    "id_pedido",
                    "uf",
                    "forma_pagamento",
                    "valor_total_pedido",
                    "data_pedido",
                )
                .orderBy("uf", "forma_pagamento", "data_pedido")
            )

            logging.info("Relatório construído com sucesso.")
            return relatorio_df

        except Exception as exc:
            logging.exception("Erro ao construir relatório de pedidos: %s", exc)
            raise
