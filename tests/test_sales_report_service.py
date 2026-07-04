from ads_client.business.sales_report_service import SalesReportService
from ads_client.schemas.pagamentos_schema import PagamentosSchema
from ads_client.schemas.pedidos_schema import PedidosSchema


def test_build_report_filters_2025_refused_and_legitimate_payments(spark):
    pedidos_data = [
        ("p1", "NOTEBOOK", 1500.0, 2, "2025-01-10T10:00:00", "SP", 1),
        ("p2", "MONITOR", 600.0, 1, "2025-01-11T10:00:00", "RJ", 2),
        ("p3", "TABLET", 1100.0, 1, "2024-01-11T10:00:00", "MG", 3),
    ]
    pagamentos_data = [
        ("p1", "PIX", 2800.0, False, "2025-01-10T10:05:00", (False, 0.10)),
        ("p2", "BOLETO", 600.0, True, "2025-01-11T10:05:00", (False, 0.20)),
        ("p3", "CARTAO_CREDITO", 1100.0, False, "2024-01-11T10:05:00", (False, 0.30)),
    ]

    pedidos_df = spark.createDataFrame(pedidos_data, PedidosSchema.build())
    pagamentos_df = spark.createDataFrame(pagamentos_data, PagamentosSchema.build())

    result = SalesReportService().build_report(pedidos_df, pagamentos_df, 2025).collect()

    assert len(result) == 1
    assert result[0]["id_pedido"] == "p1"
    assert result[0]["uf"] == "SP"
    assert result[0]["forma_pagamento"] == "PIX"
    assert result[0]["valor_total_pedido"] == 3000.0
