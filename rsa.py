import cryptography
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
import hashlib
import time

def calculate_hash_with_nonce(nickname, nonce):
    return hashlib.sha256((nickname + str(nonce)).encode('utf-8')).hexdigest()

def find_nonce_with_zeros(nickname, zeros):
    nonce = 0
    while True:
        hash_result = calculate_hash_with_nonce(nickname, nonce)
        if hash_result.startswith('0' * zeros):
            return nonce
        nonce += 1

def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

def sign_message(private_key, message):
    signature = private_key.sign(
        message.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify_signature(public_key, message, signature):
    try:
        public_key.verify(
            signature,
            message.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except:
        return False

def main():
    # 生成公私钥对
    private_key, public_key = generate_rsa_key_pair()

    # 找到满足条件的nonce
    nickname = "alex"
    nonce = find_nonce_with_zeros(nickname, 4)
    message = nickname + str(nonce)

    # 使用私钥对消息进行签名
    signature = sign_message(private_key, message)

    # 验证签名
    verified = verify_signature(public_key, message, signature)
    print("Signature verified:", verified)

if __name__ == "__main__":
    main()