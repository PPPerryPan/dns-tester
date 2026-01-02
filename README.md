# DNS Server Testing Tool

A Python tool for testing the performance and reliability of different DNS servers.

## Features

- Support for testing multiple DNS servers
- Generate test reports
- Provide real-time test progress and result summary in console
- Configurable test domain list and DNS servers

## Installation

### Requirements

- Python 3.6+
- pip

### Install Dependencies

```bash
pip install dnspython
```

## Usage

1. Clone or download the project files to your local machine

2. Configure DNS servers (optional)
   Edit the `config.py` file to customize the DNS servers and domain lists to test

3. Run the test

```bash
python main.py
```

4. View results
   - The console will display test progress and result summary
   - The generated Markdown report is located at `dns_test_results.md`

## Project Structure

```
dns-check/
├── config.py           # Configuration file (DNS servers, test domains, etc.)
├── dns_tester.py       # Core DNS testing logic
├── results_analyzer.py # Result analysis and formatting
├── report_generator.py # Markdown report generation
├── main.py             # Main entry file
├── README.md           # Project documentation
└── dns_test_results.md # Generated test report (after running)
```

## Configuration Instructions

In the `config.py` file, you can configure the following parameters:

- `dns_servers`: List of DNS servers to test
- `test_domains`: List of domains to test
- `DNS_TIMEOUT`: DNS resolution timeout (seconds)
- `DNS_LIFETIME`: DNS resolution lifetime (seconds)
- `REPORT_FILE`: Name of the generated report file

## Test Report Example

The test report contains two parts:

1. **Test Result Summary**: Shows the success rate, average response time, availability, and status of each DNS server
2. **Domains with Resolution Failures**: Lists the domains that failed to resolve for each DNS server