from config import REPORT_FILE


def generate_markdown_report(sorted_results, failed_domains):
    """
    Generate a markdown report for DNS test results
    
    Parameters:
        sorted_results: Sorted list of test results
            Format: [(dns_ip, {'success': number of successes, 'total': total domains, 'avg_time': average response time, 'availability': availability percentage, 'status': status}), ...]
        failed_domains: Information about failed domains
            Format: {dns_ip: [list of failed domains]}
    
    Returns:
        bool: Whether the report was generated successfully
    """
    try:
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            # Write title
            f.write("# DNS Server Test Results\n\n")
            
            # Write test results table (markdown format)
            f.write("## Test Results Summary\n\n")
            f.write("| DNS Server | Success/Total | Avg Time (ms) | Availability | Status |\n")
            f.write("|------------|---------------|---------------|--------------|--------|\n")
            
            for dns_ip, stat in sorted_results:
                success = stat['success']
                total = stat['total']
                avg_time = stat['avg_time']
                availability = stat['availability']
                status = stat['status']
                
                avg_time_str = f"{avg_time:.2f}" if avg_time else "Timeout"
                availability_str = f"{availability:.2f}%"
                
                f.write(f"| {dns_ip} | {success}/{total} | {avg_time_str} | {availability_str} | {status} |\n")
            
            f.write("\n")
            
            # Write failed URL records (markdown format)
            f.write("## Domains with Resolution Failures\n\n")
            
            if not failed_domains:
                f.write("All domains resolved successfully!\n\n")
            else:
                for dns_ip, domains in failed_domains.items():
                    if domains:  # Only write DNS servers with failed records
                        f.write(f"### DNS Server: {dns_ip}\n\n")
                        f.write("| Failed Domain |\n")
                        f.write("|---------------|\n")
                        for domain in domains:
                            f.write(f"| {domain} |\n")
                        f.write("\n")
        
        print(f"\nReport generated: {REPORT_FILE}")
        return True
        
    except Exception as e:
        print(f"Failed to generate report: {e}")
        return False