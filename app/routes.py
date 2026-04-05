from flask import Blueprint, jsonify, render_template, Response
from app.metrics import get_system_metrics, get_prometheus_metrics

main = Blueprint("main", __name__)


@main.route("/")
def dashboard():
    """Render the HTML dashboard."""
    metrics = get_system_metrics()
    return render_template("dashboard.html", metrics=metrics)


@main.route("/api/metrics")
def api_metrics():
    """Return raw system metrics as JSON."""
    return jsonify(get_system_metrics())


@main.route("/metrics")
def prometheus_metrics():
    """Prometheus scrape endpoint."""
    data, content_type = get_prometheus_metrics()
    return Response(data, mimetype=content_type)


@main.route("/health")
def health():
    """Liveness probe endpoint for Kubernetes."""
    return jsonify({"status": "healthy"}), 200


@main.route("/ready")
def ready():
    """Readiness probe endpoint for Kubernetes."""
    return jsonify({"status": "ready"}), 200