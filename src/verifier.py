import requests

from pkey import ProductKey

AUTHORITY = "http://localhost:8240"


def verify_pkey(key: ProductKey) -> bool:
    try:
        response = requests.post(AUTHORITY, {"key": str(key)})

        if not response.ok:
            raise ProductKeyVerificationError(f"Verification did not succeed, with a {response.status_code} HTTP error")
    except requests.exceptions.ConnectionError as ex:
        raise ProductKeyVerificationError("Verification did not succeed, authority server is offline or does not exist")

    verified = response.json()

    if not "valid" in verified:
        raise ProductKeyVerificationError(
            f"Verification almost succeeded, but the authority server did not speak any further")

    valid = verified["valid"]

    if valid is True:
        return True
    elif valid is False:
        return False

    raise ProductKeyVerificationError(
        f"Verification almost succeeded, but the authority server did not send back good data")


class ProductKeyVerificationError(Exception):
    msg: str

    def __init__(self, msg: str):
        self.msg = msg
