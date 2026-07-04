from pyspark.sql.types import BooleanType, DoubleType, StringType, StructField, StructType


class PagamentosSchema:
    """Schema explícito do dataset JSON de pagamentos."""

    @staticmethod
    def build() -> StructType:
        return StructType(
            [
                StructField("id_pedido", StringType(), False),
                StructField("forma_pagamento", StringType(), True),
                StructField("valor_pagamento", DoubleType(), True),
                StructField("status", BooleanType(), True),
                StructField("data_processamento", StringType(), True),
                StructField(
                    "avaliacao_fraude",
                    StructType(
                        [
                            StructField("fraude", BooleanType(), True),
                            StructField("score", DoubleType(), True),
                        ]
                    ),
                    True,
                ),
            ]
        )
