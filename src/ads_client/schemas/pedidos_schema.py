from pyspark.sql.types import DoubleType, LongType, StringType, StructField, StructType


class PedidosSchema:
    """Schema explícito do dataset CSV de pedidos."""

    @staticmethod
    def build() -> StructType:
        return StructType(
            [
                StructField("ID_PEDIDO", StringType(), False),
                StructField("PRODUTO", StringType(), True),
                StructField("VALOR_UNITARIO", DoubleType(), True),
                StructField("QUANTIDADE", LongType(), True),
                StructField("DATA_CRIACAO", StringType(), True),
                StructField("UF", StringType(), True),
                StructField("ID_CLIENTE", LongType(), True),
            ]
        )
