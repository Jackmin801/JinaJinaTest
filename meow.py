import random
from typing import Dict
import opentelemetry.sdk.metrics.export
import opentelemetry.sdk.metrics.view
from opentelemetry.sdk.metrics.export import AggregationTemporality, MetricExporter, MetricExportResult, MetricsData
import time
from pathlib import Path
from jina import Executor, Flow, requests, Document, DocumentArray

def test_meow():
    class DirMetricExporter(MetricExporter):
        """Implementation of :class:`MetricExporter` that prints metrics to a file in a given directory.

        This class can be used for diagnostic or testing purposes.
        """

        def __init__(
            self,
            metric_dir: str,
            preferred_temporality: Dict[type, AggregationTemporality] = None,
            preferred_aggregation: Dict[
                type, "opentelemetry.sdk.metrics.view.Aggregation"
            ] = None,
        ):
            super().__init__(
                preferred_temporality=preferred_temporality,
                preferred_aggregation=preferred_aggregation,
            )
            self.metric_filename: Path = Path(metric_dir) / str(random.randint(0, 1048575))
            self.f = open(self.metric_filename, 'a')

        def export(
            self,
            metrics_data: MetricsData,
            timeout_millis: float = 10_000,
            **kwargs,
        ) -> MetricExportResult:
            self.f.write(metrics_data.to_json())
            self.f.write('\n')
            self.f.flush()
            return MetricExportResult.SUCCESS

        def shutdown(self, timeout_millis: float = 30_000, **kwargs) -> None:
            pass

        def force_flush(self, timeout_millis: float = 10_000) -> bool:
            return True
        
        def __del__(self):
            self.f.close()

    def jerry():
        import opentelemetry.sdk.metrics.export
        from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
        from pathlib import Path

        collect_path = Path('./tmp')

        class PatchedTextReader(PeriodicExportingMetricReader):
            def __init__(self, *args, **kwargs) -> None:
                self.exporter = DirMetricExporter(collect_path)

                super().__init__(
                    exporter=self.exporter,
                    export_interval_millis=1_000,
                )

        opentelemetry.sdk.metrics.export.PeriodicExportingMetricReader = PatchedTextReader
        return Path(collect_path)


    jerry()
    from jina import Executor, Flow, requests, Document, DocumentArray

    class FirstExec(Executor):
        @requests()
        def meow(self, docs, **kwargs):
            return DocumentArray.empty(3)

    class SecondExec(Executor):
        @requests()
        def meow(self, docs, **kwargs):
            return DocumentArray.empty(3)

    with Flow(
        tracing=False,
        metrics=True,
        metrics_exporter_host='localhost',
        metrics_exporter_port=4317,
        port=12345,
    ).add(name='first_executor', uses=FirstExec, replicas=2).add(
        name="second_exec", uses=SecondExec
    ) as f:
        f.post('/')
        f.plot('flow.png')

        time.sleep(2)

