import hashlib

def get_md5(data: bytes | str) -> str:
    """Computes the MD5 hex digest for a string or bytes input."""
    # Convert string to bytes if needed
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    return hashlib.md5(data).hexdigest()

# Example Usage
text = "hello world"
print(f"MD5 digest: {get_md5(text)}")