from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    """Centraliza as configurações de entrada e saída do projeto."""

    app_name: str
    pedidos_path: str
    pagamentos_path: str
    output_path: str
    report_year: int = 2025
    write_mode: str = "overwrite"

    @classmethod
    def from_project_root(cls, root_path: str | Path = ".") -> "AppConfig":
        root = Path(root_path).resolve()
        return cls(
            app_name="relatorio-pedidos-pagamentos-recusados-legitimos",
            pedidos_path=str(root / "data/input/datasets-csv-pedidos-main/data/pedidos"),
            pagamentos_path=str(root / "data/input/dataset-json-pagamentos-main/data/pagamentos"),
            output_path=str(root / "data/output/relatorio_pedidos_2025_parquet"),
        )
