"""
Observability Module.

This module configures OpenTelemetry tracing and metrics for the FastAPI application,
and sets up a Prometheus endpoint for metric scraping.
"""

import structlog
from fastapi import FastAPI
from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from prometheus_client import make_asgi_app

logger = structlog.get_logger(__name__)


def setup_observability(
    app: FastAPI, service_name: str = "learning-analytics-api"
) -> None:
    """
    Set up observability tools for the FastAPI application.

    Args:
        app: The FastAPI application instance.
        service_name: The name of the service for tracing and metrics.
    """
    resource = Resource.create({"service.name": service_name})

    # 1. Setup Tracing
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)

    # Export traces to OTLP (e.g. Jaeger) - in dev we can fallback to console
    try:
        otlp_exporter = OTLPSpanExporter(
            endpoint="http://localhost:4317", insecure=True
        )
        span_processor = BatchSpanProcessor(otlp_exporter)
    except Exception as e:
        logger.warning(
            "Failed to setup OTLP exporter, falling back to console", error=str(e)
        )
        span_processor = BatchSpanProcessor(ConsoleSpanExporter())

    tracer_provider.add_span_processor(span_processor)

    # 2. Setup Metrics
    try:
        metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
        meter_provider = MeterProvider(
            resource=resource, metric_readers=[metric_reader]
        )
        metrics.set_meter_provider(meter_provider)
    except Exception as e:
        logger.warning("Failed to setup metrics", error=str(e))

    # 3. Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)

    # 4. Mount Prometheus /metrics endpoint
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)

    logger.info("observability_configured", service=service_name)
