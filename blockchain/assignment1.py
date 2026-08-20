import hashlib

def get_md5(data: bytes | str) -> str:

    if isinstance(data, str):
        data = data.encode('utf-8')
    
    return hashlib.md5(data).hexdigest()


text = "hello world"
print(f"MD5 digest: {get_md5(text)}")
