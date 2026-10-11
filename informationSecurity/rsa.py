from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

def generate_keypair():
    # Generate private key (2048-bit RSA)
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    # Extract public key from private key
    public_key = private_key.public_key()
    return private_key, public_key

def encrypt_rsa(plaintext: str, public_key) -> bytes:
    # Encrypt plaintext string using public key with OAEP padding
    ciphertext = public_key.encrypt(
        plaintext.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def decrypt_rsa(ciphertext: bytes, private_key) -> str:
    # Decrypt ciphertext using private key with matching OAEP padding
    decrypted_bytes = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_bytes.decode('utf-8')

# Driver Code
if __name__ == "__main__":
    msg = "NETAJISUBHASUNIVERSITYOFTECHNOLOGY"

    # Key Generation
    private_key, public_key = generate_keypair()

    # Test RSA Encryption and Decryption
    cipher_text = encrypt_rsa(msg, public_key)
    plain_text = decrypt_rsa(cipher_text, private_key)

    # Extract public exponent (e) and modulus (n) for output display
    public_numbers = public_key.public_numbers()
    
    print("=== RSA Public-Key Cryptosystem (2048-bit OAEP) ===")
    print("Plaintext :", msg)
    print("Public Exponent (e) :", public_numbers.e)
    print("Modulus (n) (hex)  :", hex(public_numbers.n)[:64] + "...")
    print("Encrypted (hex)    :", cipher_text.hex())
    print("Decrypted          :", plain_text)