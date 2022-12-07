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
    command = ["amass", "intel", "-whois", "-d", domain]
    if timeout is not None:
        command.extend(["-timeout", str(timeout)])

    try:
        # The timeout is not always respected by the amass, we enforce ours on top of it with an extra minute.
        result = subprocess.run(
            command, capture_output=True, check=False, timeout=(timeout + 1) * 60
        )
        if result.returncode != 0:
            return []
        else:
            return result.stdout.decode().splitlines()
    except subprocess.TimeoutExpired:
        return []


def enum_subdomain(domain: str, timeout: Optional[int] = None) -> List[str]:
    """Active subdomain enumeration with IP resolution to rule out invalid or old subdomains..

    Args:
        domain: Domain to lookup.
        timeout: Lookup timeout in minutes.

    Returns:
        List of subdomains.
    """
    command = ["amass", "enum", "-brute", "-min-for-recursive", "2", "-d", domain]
    if timeout is not None:
        command.extend(["-timeout", str(timeout)])

    try:
        # The timeout is not always respected by the amass, we enforce ours on top of it with an extra minute.
        result = subprocess.run(
            command, capture_output=True, check=False, timeout=(timeout + 1) * 60
        )
        if result.returncode != 0:
            return []
        else:
            return result.stdout.decode().splitlines()
    except subprocess.TimeoutExpired:
        return []
