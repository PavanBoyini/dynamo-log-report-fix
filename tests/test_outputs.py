"""
Verifier for dynamo/log-report.

Each test corresponds 1:1 to a success criterion in instruction.md:
 - test_report_file_exists_and_is_valid_json -> "write your findings to
   /app/report.json as a single JSON object"
 - test_total_request_count                  -> "total_requests: the total
   number of request lines in the log"
 - test_client_count                         -> "unique_ips: the number of
   distinct client IP addresses"
 - test_top_path                             -> "top_path: the request path
   requested more often than any other"
"""
import json
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")


def _expected_stats():
    """Independently recompute expected stats from access.log (no regex,
    to avoid mirroring the same parsing bug the solution might have)."""
    total = 0
    ips = set()
    path_counts = {}
    for line in LOG_PATH.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        total += 1
        ips.add(line.split(" ", 1)[0])
        start = line.index('"') + 1
        end = line.index('"', start)
        parts = line[start:end].split(" ")
        if len(parts) >= 2:
            path = parts[1]
            path_counts[path] = path_counts.get(path, 0) + 1
    top_path = max(path_counts, key=path_counts.get)
    return total, len(ips), top_path


def _load_report():
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"
    text = REPORT_PATH.read_text()
    assert text.strip(), "report.json is empty"
    report = json.loads(text)
    assert isinstance(report, dict), "report.json must contain a JSON object"
    return report


def test_report_file_exists_and_is_valid_json():
    """Criterion: write findings to /app/report.json as a single JSON object."""
    _load_report()


def test_total_request_count():
    """Criterion: total_requests = total number of request lines."""
    expected_total, _, _ = _expected_stats()
    report = _load_report()
    assert "total_requests" in report, "report.json missing 'total_requests'"
    assert report["total_requests"] == expected_total, (
        f"expected total_requests={expected_total}, got {report['total_requests']}"
    )


def test_client_count():
    """Criterion: unique_ips = number of distinct client IPs."""
    _, expected_clients, _ = _expected_stats()
    report = _load_report()
    assert "unique_ips" in report, "report.json missing 'unique_ips'"
    assert report["unique_ips"] == expected_clients, (
        f"expected unique_ips={expected_clients}, got {report['unique_ips']}"
    )


def test_top_path():
    """Criterion: top_path = the most-requested path."""
    _, _, expected_top = _expected_stats()
    report = _load_report()
    assert "top_path" in report, "report.json missing 'top_path'"
    assert report["top_path"] == expected_top, (
        f"expected top_path={expected_top!r}, got {report['top_path']!r}"
    )
