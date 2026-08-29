# --- Caesar Cipher ---
def encrypt_caesar(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            start = ord("A") if char.isupper() else ord("a")
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char
    return result


def decrypt_caesar(text, shift):
    return encrypt_caesar(text, -shift)


# --- Rail Fence Cipher ---
def encrypt_rail_fence(text, key):
    if key == 1:
        return text

    rails = [[] for _ in range(key)]
    row = 0
    direction = 1

    for char in text:
        rails[row].append(char)
        if row == 0:
            direction = 1
        elif row == key - 1:
            direction = -1
        row += direction

    cipher = ""
    for r in rails:
        cipher += "".join(r)
    return cipher


def decrypt_rail_fence(cipher, key):
    if key == 1:
        return cipher

    n = len(cipher)
    grid = [["" for _ in range(n)] for _ in range(key)]

    # Mark rail positions
    row = 0
    direction = 1
    for i in range(n):
        grid[row][i] = "*"
        if row == 0:
            direction = 1
        elif row == key - 1:
            direction = -1
        row += direction

    # Place cipher characters into marked positions
    idx = 0
    for r in range(key):
        for c in range(n):
            if grid[r][c] == "*" and idx < n:
                grid[r][c] = cipher[idx]
                idx += 1

    # Reconstruct original text following zig-zag order
    plain = ""
    row = 0
    direction = 1
    for i in range(n):
        plain += grid[row][i]
        if row == 0:
            direction = 1
        elif row == key - 1:
            direction = -1
        row += direction

    return plain


# Driver Code
if __name__ == "__main__":
    msg = "HELLONETWORKS"

    # Test Caesar Cipher
    caesar_enc = encrypt_caesar(msg, 3)
    caesar_dec = decrypt_caesar(caesar_enc, 3)

    print("=== Substitution Cipher (Caesar) ===")
    print("Plaintext: ", msg)
    print("Encrypted: ", caesar_enc)
    print("Decrypted: ", caesar_dec)
    print()

    # Test Rail Fence Cipher
    rail_enc = encrypt_rail_fence(msg, 3)
    rail_dec = decrypt_rail_fence(rail_enc, 3)

    print("=== Transposition Cipher (Rail Fence) ===")
    print("Plaintext: ", msg)
    print("Encrypted: ", rail_enc)
    print("Decrypted: ", rail_dec)