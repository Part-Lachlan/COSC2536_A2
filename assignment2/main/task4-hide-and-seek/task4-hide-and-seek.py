import os

# import necessary modules from pycryptodome:
# WINDOWS: pip install pycryptodome
# MAC: pip3 install pycryptodome
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

#for making paths working on all OS
BASE = os.path.dirname(os.path.abspath(__file__))

# Setup PATH variables
input_image = os.path.join(BASE, "input", "cover.jpg")
output_image = os.path.join(BASE, "output", "task4-hidden.jpg")
key_file = os.path.join(BASE, "keys", "task4-aes-key.bin")
decrypted_file = os.path.join(BASE, "output", "task4-decrypted.txt")

# Create directories if they do not exist
os.makedirs(os.path.join(BASE, "keys"), exist_ok=True)
os.makedirs(os.path.join(BASE, "output"), exist_ok=True)

# Generate AES key
def gen_AES_key():
    aes_key = get_random_bytes(32) # AES key must be either 16, 24, or 32 bytes long
    iv = get_random_bytes(16) # Initialization vector

    with open(key_file, "wb") as file:
        file.write(aes_key)

    return aes_key, iv


# Encrypt the secret message using AES
def encrypt_AES(message, aes_key, iv):
    aes_cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    padded_message = pad(message.encode("utf-8"), AES.block_size)
    ciphertext = aes_cipher.encrypt(padded_message)

    return ciphertext


# Hide encrypted message in JPEG metadata
def hide_message(iv, ciphertext):
    # Store IV and ciphertext together
    payload = iv + ciphertext

    # JPEG comment segments can hold at most 65533 bytes
    if len(payload) > 65533:
        raise ValueError("Encrypted message is too large.")

    # Read original JPEG image
    with open(input_image, "rb") as file:
        image_data = file.read()

    # Check that it is a JPEG
    if not image_data.startswith(b"\xff\xd8"):
        raise ValueError("Input file is not a JPEG image.")

    # JPEG COM marker: FF FE
    segment_length = len(payload) + 2
    comment_segment = (
        b"\xff\xfe"
        + segment_length.to_bytes(2, "big")
        + payload
    )

    # Insert data immediately after JPEG start marker
    stego_image = (
        image_data[:2]
        + comment_segment
        + image_data[2:]
    )

    #save new image with encrypted data within it
    with open(output_image, "wb") as file:
        file.write(stego_image)


# Extract encrypted message from JPEG metadata
def extract_message():
    with open(output_image, "rb") as file:
        image_data = file.read()

    # Check if image is JPEG using header
    if not image_data.startswith(b"\xff\xd8"):
        raise ValueError("Invalid JPEG image.")

    # Read the comment segment inserted after the JPEG header
    if image_data[2:4] != b"\xff\xfe":
        raise ValueError("Hidden comment segment not found.")

    segment_length = int.from_bytes(
        image_data[4:6], "big"
    )

    payload = image_data[6:4 + segment_length]

    # Extract IV and ciphertext
    iv = payload[:16]
    ciphertext = payload[16:]

    return ciphertext, iv


# Decrypt extracted message using AES
def decrypt_AES(iv, ciphertext):
    # Read saved AES key
    with open(key_file, "rb") as file:
        aes_key = file.read()

    aes_cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    padded_message = aes_cipher.decrypt(ciphertext)
    plaintext = unpad(padded_message, AES.block_size)

    decrypted_message = plaintext.decode("utf-8")

    # Save decrypted message in a separate file
    with open(decrypted_file, "w", encoding="utf-8") as file:
        file.write(decrypted_message)

    return decrypted_message


def main():
    # Get secret message from user
    message = input("Enter secret message: ")

    # Generate AES key and IV
    aes_key, iv = gen_AES_key()

    print("\nAES Key:", aes_key.hex())
    print("\nAES IV:", iv.hex())
    print("\nOriginal Message:", message)

    # Encrypt message
    ciphertext = encrypt_AES(message, aes_key, iv)

    # Print AES encrypted message
    print("\nEncrypted Message:", ciphertext.hex())

    # Hide encrypted message in JPEG
    hide_message(iv, ciphertext)

    # Print encoded image
    print("\nEncrypted message hidden in:", output_image)

    # Extract message from JPEG
    extracted_message, extracted_iv = extract_message()

    # Print extracted info from image
    print("\nExtracted IV:", extracted_iv.hex())
    print("\nExtracted Encrypted Message:", extracted_message.hex())

    # Decrypt message
    decrypted_message = decrypt_AES(extracted_iv, extracted_message)

    # Print decrypted message
    print("\nDecrypted Message:", decrypted_message)

    # Print validity check
    if message == decrypted_message:
        print("\nSUCCESS: Original and decrypted messages match.")
    else:
        print("\nERROR: Messages do not match.")


if __name__ == "__main__":
    main()
