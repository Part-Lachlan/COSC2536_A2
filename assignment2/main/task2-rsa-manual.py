import os
import os.path
import random
#for making paths working on all OS
BASE=os.path.dirname(os.path.abspath(__file__))


# Generate two different 5 digit prime numbers for p and q
def generate_prime_number():
    p = 0
    while p == 0:
        num = random.randint(10000, 99999)
        is_prime = True
         # Check if the generated number has any factors other than 1 and itself
        for i in range(2, num):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            p = num
    q = 0
    while q == 0:
        num2 = random.randint(10000, 99999)
        is_prime2 = True
         # Check if the generated number has any factors other than 1 and itself
        for i in range(2, num2):
            if num2 % i == 0:
                is_prime2 = False
                break
        # Store q only if it is prime and different from p
        if is_prime2 and num2 != p:
            q = num2
    return p, q


# Generate the RSA public and private key values
def key_generation(p,q):
    # Calculate n and phi(n)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    # Generate e and make sure it is coprime with phi(n)
    e = 0
    while e == 0:
        num = random.randint(2, phi_n - 1)
        is_coprime = True
        for i in range(2, num + 1):
            if phi_n % i == 0 and num % i == 0:
                is_coprime = False
                break
        if is_coprime:
            e = num
    # Calculate private key d
    d = pow(e,-1,phi_n)

    return e,d,n
# Encrypt the message using the RSA public key (e, n)
def encrypt_message(message, e, n):
    ciphertext = pow(message, e, n)
    return ciphertext


# Decrypt the message using the RSA private key (d, n)
def decrypt_message(ciphertext, d, n):
    decrypted_message = pow(ciphertext, d, n)
    return decrypted_message


# Main Program
# reads the input file from the input folder and stores the message in a variable named message. The message is also converted to an integer.
input_file = os.path.join(BASE, "..", "input", "task2.txt")
with open(input_file, "r") as file:
    message = file.read()
message = int(message)

# generate two different 5 digit prime numbers for the value of p and q
p,q = generate_prime_number()

# generate the RSA public and private keys
e,d,n = key_generation(p,q)

# save the RSA generated keys in the keys folder.
key_file = os.path.join(BASE, "..", "keys", "task2-keys.txt")
with open(key_file, "w") as file:
    file.write(f"Public key (n,e): ({n}, {e})\n")
    file.write(f"Private key (d): {d}")

# encrypt the message using the public key
ciphertext = encrypt_message(message,e,n)

# decrypt the ciphertext using the private key
decrypted_message = decrypt_message(ciphertext,d,n)

# saving the ciphertext and decrypted message in the output folder.
output_file = os.path.join(BASE, "..", "output", "task2-output.txt")
with open (output_file, "w") as file:
    file.write(f"Ciphertext: {ciphertext}\n")
    file.write(f"Decrypted message: {decrypted_message}")
            




