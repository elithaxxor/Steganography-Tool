from __future__ import annotations

import requests
import dns.resolver


class NetworkStego:
    """Simple HTTP header and DNS query steganography."""

    name = "network-stego"

    async def send_header(self, url: str, secret: str) -> str:
        requests.get(url, headers={"X-Secret": secret})
        return "sent"

    async def send_dns(self, domain: str, secret: str) -> str:
        qname = f"{secret}.{domain}"
        try:
            dns.resolver.resolve(qname, "A")
        except Exception:
            pass
        return "sent"
