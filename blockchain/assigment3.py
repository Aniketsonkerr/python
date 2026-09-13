import math

# Function to calculate modular inverse of 'a' mod 'm' using Extended Euclidean Algorithm
def mod_inverse(a, m):
    m0, y, x = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        y, x = x - q * y, y
    if x < 0:
        x += m0
    return x

def main():
    # 1. KEY GENERATION
    p = 23  # Prime number
    g = 5   # Primitive root (generator)
    x = 6   # Private key (1 <= x <= p-2)

    # Compute Public Key: y = (g^x) % p
    y = pow(g, x, p)

    print("=== 1. KEY GENERATION ===")
    print(f"Public Key (p, g, y) : ({p}, {g}, {y})")
    print(f"Private Key (x)      : {x}\n")

    # 2. SIGNATURE GENERATION
    m = 14  # Message hash (0 <= m <= p-1)
    k = 15  # Random secret key such that gcd(k, p-1) = 1

    # Check gcd condition
    if math.gcd(k, p - 1) != 1:
        print("Invalid k! gcd(k, p-1) must be 1.")
        return

    # Compute r = (g^k) % p
    r = pow(g, k, p)

    # Compute k^(-1) mod (p-1)
    k_inv = mod_inverse(k, p - 1)

    # Compute s = k^(-1) * (m - x * r) mod (p-1)
    temp = (m - (x * r) % (p - 1)) % (p - 1)
    s = (k_inv * temp) % (p - 1)

    print("=== 2. SIGNATURE GENERATION ===")
    print(f"Message Hash (m)     : {m}")
    print(f"Random Key (k)       : {k}")
    print(f"Digital Signature    : (r = {r}, s = {s})\n")

    # 3. SIGNATURE VERIFICATION
    print("=== 3. SIGNATURE VERIFICATION ===")

    # Range check: 0 < r < p and 0 < s < p-1
    if not (0 < r < p) or not (0 < s < p - 1):
        print("Signature Invalid: Range check failed!")
        return

    # Compute v1 = (g^m) % p
    v1 = pow(g, m, p)

    # Compute v2 = (y^r * r^s) % p
    yr = pow(y, r, p)
    rs = pow(r, s, p)
    v2 = (yr * rs) % p

    print(f"v1 (g^m mod p)       : {v1}")
    print(f"v2 (y^r * r^s mod p) : {v2}")

    if v1 == v2:
        print("\nRESULT: Signature is VALID!")
    else:
        print("\nRESULT: Signature is INVALID!")

if __name__ == "__main__":
    main()