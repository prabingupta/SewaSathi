import base64
import hashlib
import hmac
from django.conf import settings


def generate_signature(total_amount, transaction_uuid, product_code):
    """
    eSewa requires an HMAC-SHA256 signature over these three fields,
    in this exact order, base64-encoded. This proves the payment
    request actually came from us and wasn't tampered with in transit.
    """
    message = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    signature = hmac.new(
        settings.ESEWA_SECRET_KEY.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode('utf-8')


def verify_signature(data, signature, signed_field_names):
    """
    Reconstructs the same message eSewa would have signed, using only the
    fields they told us to sign (signed_field_names), then checks our own
    computed signature matches what they sent back. If this doesn't match,
    the response cannot be trusted -- it may have been tampered with.
    """
    fields = signed_field_names.split(',')
    message = ','.join(f"{field}={data.get(field, '')}" for field in fields)
    expected_signature = hmac.new(
        settings.ESEWA_SECRET_KEY.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
    expected_signature_b64 = base64.b64encode(expected_signature).decode('utf-8')
    return hmac.compare_digest(expected_signature_b64, signature)
