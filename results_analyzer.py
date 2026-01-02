def calculate_statistics(results):
    """
    Calculate statistics for DNS test results
    
    Parameters:
        results: Test results dictionary, format: {dns_ip: {'success': number of successes, 'total': total domains, 'times': [response times list]}}
    
    Returns:
        dict: Dictionary containing statistics
            Format: {dns_ip: {'success': number of successes, 'total': total domains, 'avg_time': average response time, 'availability': availability percentage, 'status': status}}
    """
    statistics = {}
    
    for dns_ip, result in results.items():
        success = result['success']
        total = result['total']
        times = result['times']
        
        # Calculate average response time
        avg_time = round(sum(times) / len(times), 2) if times else None
        
        # Calculate availability percentage
        availability = round((success / total) * 100, 2)
        
        # Determine status
        status = "✅ Good" if success == total else "⚠️  Unstable"
        
        statistics[dns_ip] = {
            'success': success,
            'total': total,
            'avg_time': avg_time,
            'availability': availability,
            'status': status
        }
    
    return statistics



def sort_results(statistics):
    """
    Sort DNS test results
    
    Parameters:
        statistics: Dictionary containing statistics
            Format: {dns_ip: {'success': number of successes, 'total': total domains, 'avg_time': average response time, ...}}
    
    Returns:
        list: Sorted results list, each element is a tuple (dns_ip, statistics)
            Sorting rule: First by success rate descending, then by average response time ascending
    """
    # Sort by success rate descending, average response time ascending
    sorted_items = sorted(
        statistics.items(),
        key=lambda item: (-item[1]['success'], item[1]['avg_time'] if item[1]['avg_time'] else float('inf'))
    )
    
    return sorted_items



def print_results(sorted_results):
    """
    Print formatted test results to console
    
    Parameters:
        sorted_results: Sorted results list, each element is a tuple (dns_ip, statistics)
    """
    # Print header
    print(f"{'DNS Server':<16} {'Success/Total':<15} {'Avg Time (ms)':<15} {'Availability':<15} {'Status'}")
    print("-" * 75)
    
    # Print each result
    for dns_ip, stat in sorted_results:
        success = stat['success']
        total = stat['total']
        avg_time = stat['avg_time']
        availability = f"{stat['availability']:.2f}%"
        status = stat['status']
        
        avg_time_str = f"{avg_time:.2f}" if avg_time else "Timeout"
        
        print(f"{dns_ip:<16} {success}/{total:<15} {avg_time_str:<15} {availability:<15} {status}")