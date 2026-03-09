"""HTTP session and headers for NCAA stats requests."""

import requests
from curl_cffi.requests import Session as CurlSession


def create_session(headers: dict | None = None) -> requests.Session:
    """
    Create a curl_cffi Session with Chrome 131 impersonation to bypass Akamai
    bot detection via TLS/HTTP2 fingerprint spoofing.

    curl_cffi sets its own browser-matching headers (UA, Accept, Sec-Fetch-*)
    automatically when default_headers=True (the default). We only add Referer
    to establish session context, since that's not set by the impersonation.
    """
    sess = CurlSession(impersonate="chrome131", default_headers=True)
    # Only add Referer — do NOT override UA or Sec-Fetch headers that
    # curl_cffi sets automatically to match the Chrome 131 fingerprint
    extra = headers or {"Referer": "https://stats.ncaa.org/"}
    sess.headers.update(extra)

    try:
        sess.get("https://stats.ncaa.org/rankings/", timeout=10)
    except Exception:
        pass

    return sess
