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
        round_times = result.get('round_times', [])
        round_avg_times = [
            round(sum(one_round_times) / len(one_round_times), 2) if one_round_times else None
            for one_round_times in round_times
        ]
        
        # Calculate availability percentage
        availability = round((success / total) * 100, 2)
        
        # Determine status
        status = "✅ Good" if success == total else "⚠️  Unstable"
        
        statistics[dns_ip] = {
            'success': success,
            'total': total,
            'avg_time': avg_time,
            'round_avg_times': round_avg_times,
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
    print(f"{'DNS Server':<16} {'Success/Total':<15} {'Avg(ms)':<10} {'R1/R2/R3 Avg(ms)':<28} {'Availability':<12} {'Status'}")
    print("-" * 105)
    
    # Print each result
    for dns_ip, stat in sorted_results:
        success = stat['success']
        total = stat['total']
        avg_time = stat['avg_time']
        round_avg_times = stat.get('round_avg_times', [])
        availability = f"{stat['availability']:.2f}%"
        status = stat['status']
        
        avg_time_str = f"{avg_time:.2f}" if avg_time else "Timeout"
        round_avg_str = "/".join(
            f"{value:.2f}" if value is not None else "NA"
            for value in round_avg_times[:3]
        )
        if not round_avg_str:
            round_avg_str = "NA"

        print(f"{dns_ip:<16} {success}/{total:<15} {avg_time_str:<10} {round_avg_str:<28} {availability:<12} {status}")