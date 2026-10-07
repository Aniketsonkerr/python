import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


def encrypt_aes(plaintext: str, key: bytes):
    # Generate a random 16-byte Initialization Vector (IV)
    iv = os.urandom(16)

    # PKCS7 padding to align text to 128-bit block boundary
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode("utf-8")) + padder.finalize()

    # Set up AES-128-CBC cipher
    cipher = Cipher(
        algorithms.AES(key), modes.CBC(iv), backend=default_backend()
    )
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv, ciphertext


def decrypt_aes(iv: bytes, ciphertext: bytes, key: bytes):
    # Set up AES-128-CBC cipher for decryption
    cipher = Cipher(
        algorithms.AES(key), modes.CBC(iv), backend=default_backend()
    )
    decryptor = cipher.decryptor()

    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove PKCS7 padding
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    return data.decode("utf-8")


# Driver Code
if __name__ == "__main__":
    msg = "NETAJISUBHASUNIVERSITYOFTECHNOLOGY"

    # Generate 16-byte (128-bit) symmetric key
    key = os.urandom(16)

    # Test AES Encryption and Decryption
    iv, cipher_text = encrypt_aes(msg, key)
    plain_text = decrypt_aes(iv, cipher_text, key)

    print("=== Advanced Encryption Standard (AES-128-CBC) ===")
    print("Plaintext :", msg)
    print("Key (hex) :", key.hex())
    print("IV (hex)  :", iv.hex())
    print("Encrypted :", cipher_text.hex())
    print("Decrypted :", plain_text)