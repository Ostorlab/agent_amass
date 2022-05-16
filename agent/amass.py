"""Wrapper for amass binary."""
from typing import List, Optional
import subprocess


def intel_whois(domain: str, timeout: Optional[int] = None) -> List[str]:
    """Perform whois reverse lookup.

    Args:
        domain: Domain to lookup.
        timeout: Lookup timeout in minutes.

    Returns:
        List of domains with same whois org.
    """
    command = ['amass', 'intel', '-whois', '-d', domain]
    if timeout is not None:
        command.extend(['-timeout', str(timeout)])

    result = subprocess.run(command, capture_output=True, check=False)
    if result.returncode != 0:
        return []
    else:
        return result.stdout.decode().splitlines()


def enum_subdomain(domain: str, timeout: Optional[int] = None) -> List[str]:
    """Active subdomain enumeration with IP resolution to rule out invalid or old subdomains..

    Args:
        domain: Domain to lookup.
        timeout: Lookup timeout in minutes.

    Returns:
        List of subdomains.
    """
    command = ['amass', 'enum', '-brute', '-min-for-recursive', '2', '-d', domain]
    if timeout is not None:
        command.extend(['-timeout', str(timeout)])

    result = subprocess.run(command, capture_output=True, check=False)
    if result.returncode != 0:
        return []
    else:
        return result.stdout.decode().splitlines()
