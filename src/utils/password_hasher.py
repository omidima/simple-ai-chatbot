import hashlib

def hash_password(password):
    # Create an MD5 hash of the password
    return hashlib.md5(password.encode()).hexdigest()