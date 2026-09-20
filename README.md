# Download Speed Tester

A small command-line script that estimates download speed by downloading the
same file multiple times. It prints the duration and downloaded size of every
request, followed by an overall summary.

The script uses only Python's standard library and does not require any runtime
dependencies.

## Requirements

- Python 3.14 or later, as specified in `pyproject.toml`
- A direct URL to a downloadable file
- An active internet connection

## Installation

Clone the repository and open its directory:

```bash
git clone <repository-url>
cd download_speed_tester
```

If you use Poetry, install the project environment with:

```bash
poetry install
```

Because the script has no third-party runtime dependencies, it can also be run
directly with a compatible Python installation.

## Usage

Pass the URL of a file as the only positional argument:

```bash
python main.py "https://example.com/large-file.zip"
```

With Poetry:

```bash
poetry run python main.py "https://example.com/large-file.zip"
```

Use a reasonably large file hosted on a fast server. A small file may produce
an inaccurate result because connection setup and network latency will account
for a significant part of the measured time.

Example output:

```text
Request 1: 2.143 sec, 10.00 MB
Request 2: 2.087 sec, 10.00 MB
...
Request 10: 2.105 sec, 10.00 MB

Average request time: 2.112 sec
Downloaded: 100.00 MB
Average speed: 4.73 MB/s
```

## How the Result Is Calculated

The script performs 10 sequential requests. For each request, it:

1. Starts a high-resolution timer.
2. Downloads the entire response into memory.
3. Stops the timer after the response has been fully read.
4. Records the elapsed time and the number of downloaded bytes.

The average request time is the arithmetic mean of all request durations:

```text
average request time = sum of request times / 10
```

The total downloaded size is converted from bytes using 1 MB = 1,048,576
bytes:

```text
total size in MB = total downloaded bytes / 1,048,576
```

The reported average download speed is calculated across all 10 requests:

```text
average speed in MB/s = total size in MB / total request time in seconds
```

Although the output uses the label `MB`, the calculation is technically based
on mebibytes (`MiB`) because it divides by 1,048,576 rather than 1,000,000.
To convert the result to megabits per second, multiply it by 8:

```text
speed in Mbit/s = speed in MB/s * 8
```

## Notes and Limitations

- The target file is downloaded 10 times, so the test transfers approximately
  10 times the file size. Consider this when using a metered connection.
- Each response is loaded completely into memory. Avoid files that are too large
  for the available RAM.
- Results depend on the remote server, routing, Wi-Fi quality, concurrent network
  traffic, and connection setup overhead. They do not represent a controlled
  benchmark of the internet connection alone.
- The script disables TLS certificate verification. Use only URLs and servers
  that you trust.
- HTTP and network errors are not retried; an error stops the test.
