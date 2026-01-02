from config import dns_servers, test_domains
from dns_tester import run_all_tests
from results_analyzer import calculate_statistics, sort_results, print_results
from report_generator import generate_markdown_report


def main():
    """
    Main function that integrates all DNS testing processes
    """
    print("=" * 60)
    print("DNS Server Testing Program")
    print("=" * 60)
    print(f"Number of test domains: {len(test_domains)}")
    print(f"Number of test DNS servers: {len(dns_servers)}")
    print("=" * 60)
    
    # 1. Run DNS tests
    print("Starting DNS server tests...\n")
    all_results, all_failed_domains = run_all_tests(dns_servers, test_domains)
    
    # 2. Analyze test results
    print("\nAnalyzing test results...")
    statistics = calculate_statistics(all_results)
    
    # 3. Sort and print results
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    sorted_results = sort_results(statistics)
    print_results(sorted_results)
    
    # 4. Generate markdown report
    print("\n" + "=" * 60)
    print("Generating test report...")
    generate_markdown_report(sorted_results, all_failed_domains)
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()