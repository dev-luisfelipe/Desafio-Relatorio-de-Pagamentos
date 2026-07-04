from pyspark.sql import DataFrame


class DataWriter:
    """Realiza escrita dos resultados do pipeline."""

    def write_parquet(self, dataframe: DataFrame, output_path: str, mode: str = "overwrite") -> None:
        dataframe.write.mode(mode).parquet(output_path)
