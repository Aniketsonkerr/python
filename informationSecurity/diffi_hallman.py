from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

def generate_parameters():
    # Generate 2048-bit DH domain parameters (prime p and generator g)
    parameters = dh.generate_parameters(generator=2, key_size=2048)
    return parameters

def generate_keypair(parameters):
    # Generate DH private key and extract matching public key
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key

def compute_shared_secret(private_key, peer_public_key) -> bytes:
    # Compute raw DH shared secret and derive key using HKDF-SHA256
    raw_shared_key = private_key.exchange(peer_public_key)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'dh key exchange',
    ).derive(raw_shared_key)
    return derived_key

# Driver Code
if __name__ == "__main__":
    # Parameter Generation
    parameters = generate_parameters()
    param_numbers = parameters.parameter_numbers()
    p, g = param_numbers.p, param_numbers.g

    # Key Generation for Alice and Bob
    alice_private, alice_public = generate_keypair(parameters)
    bob_private, bob_public = generate_keypair(parameters)

    # Extract public key values for display
    alice_y = alice_public.public_numbers().y
    bob_y = bob_public.public_numbers().y

    # Shared Key Exchange and Computation
    alice_shared_key = compute_shared_secret(alice_private, bob_public)
    bob_shared_key = compute_shared_secret(bob_private, alice_public)

    print("=== Diffie-Hellman Key Exchange (2048-bit DH with HKDF) ===")
    print("Modulus (p) (hex)  :", hex(p)[:64] + "...")
    print("Generator (g)      :", g)
    print("Alice Public Key   :", hex(alice_y)[:64] + "...")
    print("Bob Public Key     :", hex(bob_y)[:64] + "...")
    print("Alice Shared Key   :", alice_shared_key.hex())
    print("Bob Shared Key     :", bob_shared_key.hex())
    print("Keys Match         :", alice_shared_key == bob_shared_key)