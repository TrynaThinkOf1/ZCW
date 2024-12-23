import hashlib

def hashPasskey(passkey):
    passkey = passkey.encode('utf-8')
    return hashlib.sha256(passkey).hexdigest()