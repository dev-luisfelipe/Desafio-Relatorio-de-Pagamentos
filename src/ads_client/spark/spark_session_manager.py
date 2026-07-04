from pyspark.sql import SparkSession


class SparkSessionManager:
    """Gerencia a criação e o encerramento da sessão Spark."""

    def __init__(self, app_name: str, master: str = "local[*]") -> None:
        self.app_name = app_name
        self.master = master
        self._spark: SparkSession | None = None

    def get_or_create(self) -> SparkSession:
        self._spark = (
            SparkSession.builder.appName(self.app_name)
            .master(self.master)
            .config("spark.sql.session.timeZone", "UTC")
            .getOrCreate()
        )
        return self._spark

    def stop(self) -> None:
        if self._spark is not None:
            self._spark.stop()
            self._spark = None
