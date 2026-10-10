import os

# import necessary modules from pycryptodome:
# WINDOWS: pip install pycryptodome
# MAC: pip3 install pycryptodome
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


#for making paths working on all OS
BASE=os.path.dirname(os.path.abspath(__file__))

# Setup PATH variables (based on L5/rsa_pycryptodome_file.py)
input_file = os.path.join(BASE, "..", "task2-rsa-manual", "input", "task2.txt")

public_key_file = os.path.join(BASE, "keys", "task3-public.pem")
private_key_file = os.path.join(BASE, "keys", "task3-private.pem")
encrypted_file = os.path.join(BASE, "output", "task3-encrypted.bin")
encrypted_aes_key_file = os.path.join(BASE, "output", "task3-encrypted-aes-key.bin")
decrypted_file = os.path.join(BASE, "output", "task3-decrypted.txt")

# Create directories if they do not exist
os.makedirs(os.path.join(BASE, "keys"), exist_ok=True)
os.makedirs(os.path.join(BASE, "output"), exist_ok=True)

# Get task2.txt with "rb" for bytes
with open(input_file, "rb") as file:
    plaintext = file.read()

# Generate RSA keys:
def gen_RSA_keys():
    rsa_key = RSA.generate(2048)
    private_key = rsa_key.export_key()
    public_key = rsa_key.publickey().export_key()

    # Save RSA keys into separate files
    with open(private_key_file, "wb") as file:
        file.write(private_key)
    with open(public_key_file, "wb") as file:
        file.write(public_key)

    return private_key, public_key

# Generate AES key (code based on example in L5/aes_ofb_string.py):
def gen_AES_key():
    aes_key = get_random_bytes(32) # AES key must be either 16, 24, or 32 bytes long
    iv = get_random_bytes(16) # Initialization vector

    return aes_key, iv

# Encrypt with AES (code based on example in L5/aes_cbc_file.py):
def encrypt_AES(aes_key, iv):
    aes_cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    padded_plaintext = pad(plaintext, AES.block_size)
    ciphertext = aes_cipher.encrypt(padded_plaintext)

    # Store IV + encrypted file data
    with open(encrypted_file, "wb") as file:
        file.write(iv + ciphertext)

    return ciphertext

# Encrypt with RSA (code based on example in L5/rsa_pycryptodome_file.py):
def encrypt_RSA(public_key, aes_key):
    rsa_public_key = RSA.import_key(public_key)
    rsa_encrypt_cipher = PKCS1_OAEP.new(rsa_public_key) # OAEP padding - NOT textbook RSA as per Q3 req

    encrypted_aes_key = rsa_encrypt_cipher.encrypt(aes_key)

    # Save encrypted AES key
    with open(encrypted_aes_key_file, "wb") as file:
        file.write(encrypted_aes_key)

    return encrypted_aes_key

def decrypt_RSA(encrypted_aes_key):
    with open(private_key_file, "rb") as file:
        saved_private_key = RSA.import_key(file.read())

    rsa_decrypted_cipher = PKCS1_OAEP.new(saved_private_key)

    decrypted_aes_key = rsa_decrypted_cipher.decrypt(encrypted_aes_key)

    return decrypted_aes_key

def decrypt_AES(decrypted_key):
    with open(encrypted_file, "rb") as file:
        stored_iv = file.read(16)
        stored_ciphertext = file.read()

    aes_decrypt_cipher = AES.new(decrypted_key, AES.MODE_CBC, stored_iv)

    padded_decrypted_data = aes_decrypt_cipher.decrypt(stored_ciphertext)

    decrypted_data = unpad(padded_decrypted_data, AES.block_size)

    #save decrypted file
    with open(decrypted_file, "wb") as file:
        file.write(decrypted_data)

    return decrypted_data

def main():
    # Generate keys
    aes_key, iv = gen_AES_key()
    private_rsa_key, public_rsa_key = gen_RSA_keys()

    # Print keys (using .hex() and .decode() for print readability)
    print("AES key: ", aes_key.hex(), "\n")
    print("Private RSA key:\n", private_rsa_key.decode(), "\n")
    print("Public RSA key:\n", public_rsa_key.decode(), "\n")

    # Encode
    ciphertext = encrypt_AES(aes_key, iv)
    encrypted_key = encrypt_RSA(public_rsa_key,aes_key)

    # Print encoded
    print("Encrypted AES cipher key (RSA): ", encrypted_key.hex(), "\n")
    print("Encrypted Data:", ciphertext.hex())

    # Decode
    decrypted_key = decrypt_RSA(encrypted_key)
    decrypted_data = decrypt_AES(decrypted_key)

    # Print decoded
    print("\nDecrypted AES key: ", decrypted_key.hex())
    print("\nDecrypted Data: ", decrypted_data.decode())

    # Print validity check
    if plaintext == decrypted_data:
        print("\n SUCCESS: Decrypted file matches original file")
    else:
        print("\n ERROR: Decrypted file does not match original file")

if __name__ == "__main__":
    main()
