from flask import Flask, Response
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Resource/Provider
resource = Resource.create({
    "service.name": "app-python",
    "service.version": "1.0.0",
    "deployment.environment": "lab"
})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

# Tracing exporter -> OTel Collector
otlp_exporter = OTLPSpanExporter(endpoint="otel-collector:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(span_processor)

# Auto-instrument Flask
FlaskInstrumentor().instrument_app(app)

# Prometheus metrics
REQUEST_COUNTER = Counter('app_requests_total', 'Total number of requests')

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route("/")
def hello():
    REQUEST_COUNTER.inc()
    return "Santo piripillo!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
