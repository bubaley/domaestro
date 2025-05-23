import requests

from app.core.settings import SETTINGS


def check_cname_a_record(domain: str) -> tuple[bool, str]:
    """
    Checks CNAME and A records for a domain using Google DNS API.

    Args:
        domain: Domain name to check

    Returns:
        tuple[bool, str]: (success status, message)
    """
    try:
        cname_response = requests.get(
            'https://dns.google/resolve',
            params={'name': domain, 'type': 'CNAME'},
            headers={'Accept': 'application/dns-json'},
            timeout=10,
        )
        cname_response.raise_for_status()
        cname_data = cname_response.json()

        if cname_data.get('Status') == 0 and 'Answer' in cname_data:
            # CNAME record found
            cname_answer = cname_data['Answer'][0]
            cname = cname_answer['data'].rstrip('.')  # Remove trailing dot
            if cname not in SETTINGS.valid_cnames:
                return False, f'CNAME record {cname} is not in the list of valid CNAMEs.'
            return True, f'CNAME record found: {cname}'
    except requests.RequestException as e:
        return False, f'Error checking CNAME via Google DNS: {e}'
    except (KeyError, IndexError, ValueError):
        # CNAME not found or parsing error, proceed to check A record
        pass

    # If CNAME not found, check A record
    try:
        a_response = requests.get(
            'https://dns.google/resolve',
            params={'name': domain, 'type': 'A'},
            headers={'Accept': 'application/dns-json'},
            timeout=10,
        )
        a_response.raise_for_status()
        a_data = a_response.json()

        if a_data.get('Status') == 0 and 'Answer' in a_data:
            # A records found
            ips = [answer['data'] for answer in a_data['Answer']]
            invalid_ips = [ip for ip in ips if ip not in SETTINGS.valid_ips]
            if invalid_ips:
                return (
                    False,
                    f'A record(s) {", ".join(invalid_ips)} are not in the list of valid IPs: {", ".join(SETTINGS.valid_ips)}',
                )
            return True, f'A record(s) found: {", ".join(ips)}'
        else:
            return False, f'No A records found for domain {domain}'

    except requests.RequestException as e:
        return False, f'Error checking A record via Google DNS: {e}'
    except (KeyError, IndexError, ValueError) as e:
        return False, f'Error parsing DNS response: {e}'
