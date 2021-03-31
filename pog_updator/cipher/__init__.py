from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import os

dir_path = os.path.abspath(os.path.dirname(__file__))

bin_list = {
    'main_db_endpoint': 'main_db_endpoint.bin',
    'test_db_endpoint': 'test_db_endpoint.bin',
    'postgres_key': 'postgres_key.bin',
    'redis_key': 'redis_key.bin',
}

pem_list = {
    'private': 'private.pem',
    'public': 'public.pem',
}

def decrypt_cipher_file(bin_file_path, pem_file_path):
    file_in = open(bin_file_path, "rb")
    private_key = RSA.import_key(open(pem_file_path).read())

    enc_session_key, nonce, tag, ciphertext = \
       [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_GCM, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    return data.decode('utf-8')

def get(name, pem='private'):
    bin_file_path = os.path.join(dir_path, bin_list[name])
    pem_file_path = os.path.join(dir_path, pem_list[pem])
    return decrypt_cipher_file(bin_file_path, pem_file_path)
