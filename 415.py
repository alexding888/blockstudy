import flask
import hashlib
import time

def calculate_hash_with_nonce(nonce):
    return hashlib.sha256(('alex' + str(nonce)).encode('utf-8')).hexdigest()

def find_hash_with_zeros(zeros):
    nonce = 0
    start_time = time.time()
    while True:
        hash_result = calculate_hash_with_nonce(nonce)
        if hash_result.startswith('0' * zeros):
            end_time = time.time()
            print(f"Found hash with {zeros} zeros: {hash_result}")
            print(f"Time taken: {end_time - start_time} seconds")
            break
        nonce += 1

find_hash_with_zeros(4)
find_hash_with_zeros(5)

import flask

