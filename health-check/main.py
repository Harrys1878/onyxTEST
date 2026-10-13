import sys

from healthcheck.checker import check_endpoint


def main():
    checks = [
        {
            "name": "Onyx Application",
            "url": "https://p01--onyx-frontend-test--xgrwlpwkjwrz.code.run/"
        },
        {
            "name": "Onyx Backend API",
            "url": "https://p01--onyx-nginx-test--xgrwlpwkjwrz.code.run/api/health"
        },
    ]

    results = []

    for check in checks:
        result = check_endpoint(
            name=check["name"],
            url=check["url"]
        )
        results.append(result)

    print("\nOnyx Health Check")
    print("-" * 60)

    for result in results:
        status = "PASS" if result["healthy"] else "FAIL"

        print(
            f'{result["name"]:<25} '
            f'{status:<6} '
            f'{str(result["status_code"]):<6} '
            f'{str(result["response_time_ms"]):<8}ms '
            f'{result["message"]}'
        )

    print("-" * 60)

    overall_healthy = all(
        result["healthy"] for result in results
    )

    if overall_healthy:
        print("Overall status: HEALTHY")
        sys.exit(0)

    print("Overall status: UNHEALTHY")
    sys.exit(1)


if __name__ == "__main__":
    main()