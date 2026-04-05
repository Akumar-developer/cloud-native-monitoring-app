import psutil
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST

# --- Prometheus Gauges ---
CPU_USAGE = Gauge("system_cpu_usage_percent", "System CPU usage in percent")
MEMORY_USAGE = Gauge("system_memory_usage_percent", "System memory usage in percent")
MEMORY_USED = Gauge("system_memory_used_bytes", "System memory used in bytes")
MEMORY_TOTAL = Gauge("system_memory_total_bytes", "System memory total in bytes")
DISK_USAGE = Gauge("system_disk_usage_percent", "System disk usage in percent")


def get_system_metrics() -> dict:
    """Collect and return current system metrics."""
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    metrics = {
        "cpu": {
            "usage_percent": cpu,
            "core_count": psutil.cpu_count(logical=False),
            "logical_count": psutil.cpu_count(logical=True),
        },
        "memory": {
            "usage_percent": memory.percent,
            "used_gb": round(memory.used / (1024**3), 2),
            "total_gb": round(memory.total / (1024**3), 2),
            "available_gb": round(memory.available / (1024**3), 2),
        },
        "disk": {
            "usage_percent": disk.percent,
            "used_gb": round(disk.used / (1024**3), 2),
            "total_gb": round(disk.total / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
        },
    }

    # Update Prometheus gauges
    CPU_USAGE.set(cpu)
    MEMORY_USAGE.set(memory.percent)
    MEMORY_USED.set(memory.used)
    MEMORY_TOTAL.set(memory.total)
    DISK_USAGE.set(disk.percent)

    return metrics


def get_prometheus_metrics():
    """Return Prometheus-formatted metrics."""
    get_system_metrics()  # Refresh gauges before scrape
    return generate_latest(), CONTENT_TYPE_LATEST