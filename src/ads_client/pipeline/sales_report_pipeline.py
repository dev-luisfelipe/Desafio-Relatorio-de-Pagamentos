from ads_client.config.app_config import AppConfig
from ads_client.business.sales_report_service import SalesReportService
from ads_client.io.data_reader import DataReader
from ads_client.io.data_writer import DataWriter
from ads_client.schemas.pagamentos_schema import PagamentosSchema
from ads_client.schemas.pedidos_schema import PedidosSchema


class SalesReportPipeline:
    """Orquestra leitura, transformação e escrita do relatório."""

    def __init__(
        self,
        config: AppConfig,
        reader: DataReader,
        writer: DataWriter,
        service: SalesReportService,
        pedidos_schema: PedidosSchema,
        pagamentos_schema: PagamentosSchema,
    ) -> None:
        self.config = config
        self.reader = reader
        self.writer = writer
        self.service = service
        self.pedidos_schema = pedidos_schema
        self.pagamentos_schema = pagamentos_schema

    def run(self) -> None:
        pedidos_df = self.reader.read_pedidos(
            self.config.pedidos_path,
            self.pedidos_schema.build(),
        )
        pagamentos_df = self.reader.read_pagamentos(
            self.config.pagamentos_path,
            self.pagamentos_schema.build(),
        )
        report_df = self.service.build_report(pedidos_df, pagamentos_df, self.config.report_year)
        self.writer.write_parquet(report_df, self.config.output_path, self.config.write_mode)
