import argparse
import ssl
import time
import urllib.request


REQUEST_COUNT = 10
MB = 1024 * 1024

ssl_context = ssl._create_unverified_context()


def measure_speed(url: str) -> None:
    request_times = []
    total_bytes = 0
    total_time = 0.0

    for i in range(REQUEST_COUNT):
        start_time = time.perf_counter()

        with urllib.request.urlopen(url, context=ssl_context) as response:
            data = response.read()

        elapsed_time = time.perf_counter() - start_time

        downloaded_bytes = len(data)

        request_times.append(elapsed_time)
        total_bytes += downloaded_bytes
        total_time += elapsed_time

        print(
            f"Request {i + 1}: "
            f"{elapsed_time:.3f} sec, "
            f"{downloaded_bytes / MB:.2f} MB"
        )

    average_time = sum(request_times) / REQUEST_COUNT
    total_mb = total_bytes / MB
    speed_mbps = total_mb / total_time

    print()
    print(f"Average request time: {average_time:.3f} sec")
    print(f"Downloaded: {total_mb:.2f} MB")
    print(f"Average speed: {speed_mbps:.2f} MB/s")


def main():
    parser = argparse.ArgumentParser(
        description="Simple internet download speed tester"
    )

    parser.add_argument(
        "url",
        help="URL of a large file to download"
    )

    args = parser.parse_args()

    measure_speed(args.url)


if __name__ == "__main__":
    main()