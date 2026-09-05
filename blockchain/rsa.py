import hashlib


def extended_gcd(a: int, b: int):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    return gcd, y1, x1 - (a // b) * y1


def mod_inverse(e: int, phi: int) -> int:
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist.")
    return (x % phi + phi) % phi


def generate_rsa_keys(p: int, q: int):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 17  # Common coprime candidate
    d = mod_inverse(e, phi)
    return (e, n), (d, n)


def hash_message(message: str) -> int:
    # Compute SHA-256 hash integer representation
    digest = hashlib.sha256(message.encode()).hexdigest()
    return int(digest, 16)


def sign_message(message: str, private_key: tuple) -> int:
    d, n = private_key
    m_hash = hash_message(message) % n
    signature = pow(m_hash, d, n)
    return signature


def verify_signature(message: str, signature: int, public_key: tuple) -> bool:
    e, n = public_key
    m_hash = hash_message(message) % n
    decrypted_hash = pow(signature, e, n)
    return m_hash == decrypted_hash


if __name__ == "__main__":
    # Key Generation using prime numbers p = 61 and q = 53
    public_key, private_key = generate_rsa_keys(61, 53)

    message = "CONFIDENTIAL_DATA"
    signature = sign_message(message, private_key)

    print("=== RSA Key Pair Generation ===")
    print(f"Public Key (e, n)  : {public_key}")
    print(f"Private Key (d, n) : {private_key}\n")

    print("=== Digital Signature Generation & Verification ===")
    print(f"Original Message   : {message}")
    print(f"Digital Signature  : {signature}\n")

    # Verification on valid data
    is_valid = verify_signature(message, signature, public_key)
    print(
        f"Verification (Original Message) : {'SUCCESS' if is_valid else 'FAILED'}"
    )

    # Verification on tampered data
    tampered_message = "CONFIDENTIAL_DATE"
    is_tampered_valid = verify_signature(
        tampered_message, signature, public_key
    )
    print(
        f"Verification (Tampered Message) : {'SUCCESS' if is_tampered_valid else 'FAILED'}"
    )