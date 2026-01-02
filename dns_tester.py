import dns.resolver
import time
from collections import defaultdict
from config import DNS_TIMEOUT, DNS_LIFETIME


def test_dns_server(dns_ip, domains):
    """
    Test a single DNS server's ability to resolve specified domains
    
    Parameters:
        dns_ip: DNS server IP address
        domains: List of domains to test
    
    Returns:
        tuple: (result dictionary, list of failed domains)
            Result dictionary format: {'success': number of successful resolutions, 'total': total domains, 'times': [response times list]}
    """
    print(f"Testing DNS server: {dns_ip}")
    
    # Initialize DNS resolver
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = [dns_ip]
    resolver.timeout = DNS_TIMEOUT
    resolver.lifetime = DNS_LIFETIME
    
    # Initialize result records
    result = {'success': 0, 'total': 0, 'times': []}
    failed_domains = []
    
    # Test each domain
    for domain in domains:
        print(f"  Resolving domain: {domain}")
        start = time.time()
        
        try:
            # Attempt to resolve domain
            answers = resolver.resolve(domain)
            elapsed = (time.time() - start) * 1000  # Convert to milliseconds
            
            # Update success records
            result['success'] += 1
            result['times'].append(elapsed)
            print(f"    Success: {elapsed:.2f} ms")
            
        except Exception as e:
            # Update failure records
            failed_domains.append(domain)
            print(f"    Failed: {e}")
        
        result['total'] += 1
    
    return result, failed_domains



def run_all_tests(dns_servers, domains):
    """
    Run tests for all DNS servers
    
    Parameters:
        dns_servers: List of DNS servers
        domains: List of domains to test
    
    Returns:
        tuple: (all results dictionary, failed domains dictionary)
            All results dictionary format: {dns_ip: {'success': number of successful resolutions, 'total': total domains, 'times': [response times list]}}
            Failed domains dictionary format: {dns_ip: [list of failed domains]}
    """
    all_results = defaultdict(dict)
    all_failed_domains = defaultdict(list)
    
    for dns_ip in dns_servers:
        result, failed_domains = test_dns_server(dns_ip, domains)
        all_results[dns_ip] = result
        if failed_domains:
            all_failed_domains[dns_ip] = failed_domains
    
    return all_results, all_failed_domains