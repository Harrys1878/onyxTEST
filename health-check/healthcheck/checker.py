import time
import requests


def check_endpoint(name: str, url: str) -> dict:
    start_time = time.perf_counter()

    try:
        response = requests.get(url, timeout=5)

        response_time_ms = int(
            (time.perf_counter() - start_time) * 1000
        )

        return {
            "name": name,
            "healthy": response.status_code == 200,
            "status_code": response.status_code,
            "message": "OK" if response.status_code == 200 else "Unhealthy response",
            "response_time_ms": response_time_ms,
        }

    except requests.Timeout:
        return {
            "name": name,
            "healthy": False,
            "status_code": None,
            "message": "Request timed out",
            "response_time_ms": None,
        }

    except requests.ConnectionError:
        return {
            "name": name,
            "healthy": False,
            "status_code": None,
            "message": "Connection failed",
            "response_time_ms": None,
        }