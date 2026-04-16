import dns.resolver
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
from config import DNS_TIMEOUT, DNS_LIFETIME, TEST_ROUNDS, DNS_MAX_WORKERS


def resolve_domain_once(dns_ip, domain):
    """
    Resolve one domain once using the specified DNS server.

    Returns:
        tuple: (domain, success, elapsed_ms, error_message)
    """
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = [dns_ip]
    resolver.timeout = DNS_TIMEOUT
    resolver.lifetime = DNS_LIFETIME

    start = time.time()
    try:
        resolver.resolve(domain)
        elapsed = (time.time() - start) * 1000
        return domain, True, elapsed, None
    except Exception as e:
        return domain, False, None, str(e)


def test_dns_server(dns_ip, domains, rounds=TEST_ROUNDS, max_workers=DNS_MAX_WORKERS):
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
    
    # Initialize result records
    result = {'success': 0, 'total': 0, 'times': [], 'round_times': [[] for _ in range(rounds)]}
    failed_domains = set()

    worker_count = max(1, min(max_workers, len(domains)))

    # Run full-domain batches across rounds to reduce immediate cache effects
    for round_idx in range(rounds):
        print(f"  Starting round {round_idx + 1}/{rounds} with {worker_count} workers")
        round_success = 0
        round_failed = 0

        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            futures = [executor.submit(resolve_domain_once, dns_ip, domain) for domain in domains]
            for future in as_completed(futures):
                domain, success, elapsed, error = future.result()
                result['total'] += 1
                if success:
                    result['success'] += 1
                    result['times'].append(elapsed)
                    result['round_times'][round_idx].append(elapsed)
                    round_success += 1
                else:
                    failed_domains.add(domain)
                    round_failed += 1
                    print(f"    Failed domain: {domain} ({error})")

        print(f"  Round {round_idx + 1}/{rounds} done: success={round_success}, failed={round_failed}")

    return result, sorted(failed_domains)



def run_all_tests(dns_servers, domains, rounds=TEST_ROUNDS, max_workers=DNS_MAX_WORKERS):
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
        result, failed_domains = test_dns_server(
            dns_ip,
            domains,
            rounds=rounds,
            max_workers=max_workers
        )
        all_results[dns_ip] = result
        if failed_domains:
            all_failed_domains[dns_ip] = failed_domains
    
    return all_results, all_failed_domains