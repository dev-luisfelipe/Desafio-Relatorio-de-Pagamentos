from pathlib import Path

from ads_client.business.sales_report_service import SalesReportService
from ads_client.config.app_config import AppConfig
from ads_client.io.data_reader import DataReader
from ads_client.io.data_writer import DataWriter
from ads_client.pipeline.sales_report_pipeline import SalesReportPipeline
from ads_client.schemas.pagamentos_schema import PagamentosSchema
from ads_client.schemas.pedidos_schema import PedidosSchema
from ads_client.spark.spark_session_manager import SparkSessionManager


def main() -> None:
    """Aggregation Root: instancia e injeta todas as dependências."""
    project_root = Path(__file__).resolve().parents[1]
    config = AppConfig.from_project_root(project_root)

    spark_manager = SparkSessionManager(config.app_name)
    spark = spark_manager.get_or_create()

    try:
        reader = DataReader(spark)
        writer = DataWriter()
        service = SalesReportService()
        pedidos_schema = PedidosSchema()
        pagamentos_schema = PagamentosSchema()

        pipeline = SalesReportPipeline(
            config=config,
            reader=reader,
            writer=writer,
            service=service,
            pedidos_schema=pedidos_schema,
            pagamentos_schema=pagamentos_schema,
        )
        pipeline.run()
    finally:
        spark_manager.stop()


if __name__ == "__main__":
    main()
