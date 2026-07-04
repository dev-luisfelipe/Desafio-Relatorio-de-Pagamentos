from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType


class DataReader:
    """Realiza leitura de dados com schemas explícitos e sem inferência."""

    def __init__(self, spark: SparkSession) -> None:
        self.spark = spark

    def read_pedidos(self, path: str, schema: StructType) -> DataFrame:
        return (
            self.spark.read.format("csv")
            .option("header", True)
            .option("sep", ";")
            .option("compression", "gzip")
            .schema(schema)
            .load(path)
        )

    def read_pagamentos(self, path: str, schema: StructType) -> DataFrame:
        return (
            self.spark.read.format("json")
            .option("compression", "gzip")
            .schema(schema)
            .load(path)
        )
