from pathlib import Path
from typing import Dict
from opentelemetry.sdk.metrics.export import MetricsData
import json


def get_metrics(metric_dir: Path, service_name: str) -> Dict:
    for metric_file in metric_dir.glob("*"):
        with open(metric_file, "r") as f:
            first_line = json.loads(f.readline())
            cur_service_name = first_line['resource_metrics'][0]['resource']['attributes']['service.name']
            
            print(first_line)
            print(service_name)
            if cur_service_name != service_name:
                continue

get_metrics(Path('./tmp'), 'gateway/rep-0')
