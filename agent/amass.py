"""Wrapper for amass binary."""
from typing import Iterator
import subprocess


def intel_whois(domain: str, timeout: int | None = None) -> list[str]:
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


def enum_subdomain(domain: str, timeout: int | None = None) -> Iterator[str]:
    """Active subdomain enumeration with IP resolution to rule out invalid or old subdomains.

    Args:
        domain: Domain to lookup.
        timeout: Lookup timeout in minutes.

    Returns:
        List of subdomains.
    """
    command = ["amass", "enum", "-brute", "-norecursive", "-d", domain]
    if timeout is not None:
        command.extend(["-timeout", str(timeout)])

    # The timeout is not always respected by the amass, we enforce ours on top of it with an extra minute.
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True
    )
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        print("XXX", output)
        if output:
            if "FQDN" in output:
                yield output.strip().split(" ")[0]


