# REFERENCE: "import os" was referenced from the Week 7 lectorial code, file: "rsa_padding_file.py".
import os
import random
import Crypto.Util.number

# REFERENCE: The BASE path approach was referenced from the Week 7 lectorial code, file: "rsa_padding_file.py".
# For making paths working on all OS
BASE=os.path.dirname(os.path.abspath(__file__))

def handling_user_input(plaintext):
    # Converting the plaintext string into its numerical representation by converting each character to ASCII value and joining them togather.
    string_result = ""
    for i in plaintext:
        ascii_value  = ord(i)
        string_result =  string_result + str(ascii_value)
    final_integer = int(string_result)
    return final_integer
    

          

     

def generate_public_key(p, q):
    # calculating n/modulus and phi(n)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    # seting public exponent e to a common vlaue of 65537
    e = 65537

    # checking if e is coprime with phi(n)
    compatible_public_exponent = True
    for i in range(2, e + 1):
        if phi_n % i == 0 and e % i == 0:
            compatible_public_exponent = False
            break

    # If e is not coprime with phi(n), generate a new e value
    if compatible_public_exponent == False:
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
    return e, n

def encrypt_plaintext(plaintext, e, n):
     # Encrypt the plaintext using the RSA public key (e, n)
     ciphertext = pow(plaintext, e ,n)
     return ciphertext

def handling_first_and_last_name():
    # Prompts the user to enter their first and last name, and checks if the input contains anything other than chracters from a-z or A-Z. If the input is invalid it reprompts them
    correct_name = False
    while correct_name == False:
        full_name = input("Enter your first and last name: " )
        name_check = full_name.replace(" ","")
        name_check_2 = full_name.split()
        if name_check.isalpha() == True and len(name_check_2) == 2:
            correct_name = True
    return full_name

# Function ensures that the given number is an integer, within the specified range and is a prime number.
def handling_prime_input(prime_number, min_value, max_value):
    is_prime = False
    while is_prime == False:
        Prime = input(f"Enter prime {prime_number} number between {min_value} and {max_value}: ")
        is_digit = Prime.isdigit()
        if is_digit == False:
            print("The input is not a number")
            continue
        Prime = int(Prime)
        if Prime < min_value or Prime > max_value:
            print(f"The number is not in the range of {min_value} and {max_value}")
            continue
        is_prime = Crypto.Util.number.isPrime(Prime)
        if is_prime == False:
            print("The number is not prime")
    return Prime


# Main
# ensures that the student ID entered by the user is only numbers.
valid_id = False
while valid_id == False:
    student_id = input("Enter your student ID (numbers only): ")
    if student_id.isdigit() == True:
        valid_id = True
print(f"Student ID : {student_id}")

# Prompts the user to enter their first and last namee, if input is invalid it repormmpts them. Then it extracts the intials from the first and last name and captialises them.
full_name = handling_first_and_last_name()
first_name, last_name = full_name.split()
initials = (first_name[0] + last_name[0]).upper()
# prints the initials of the user
print("Your initials are: ", initials)

# gets the two prime numbers from the user and checks if they are valid.
# The primes are far apart and from different ranges to address the close-prime weakness identified in Question 7.1.
prime_1 = handling_prime_input(1, 1000000000, 9999999999)
prime_2 = handling_prime_input(2, 10000000000000, 99999999999999 )

# ensures the plain text is only alphabets.
accept_plaintext = False
while accept_plaintext == False:
    plaintext = input("Enter data using alphabetic characters only (at least 3 characters): ")
    if plaintext.isalpha() == True and len(plaintext) >= 3:
        accept_plaintext = True
# displays the plaintext entered by the user
print(f"Plaintext: {plaintext}")

# generate the public key values e and n
e, n = generate_public_key(prime_1, prime_2)

plaintext_int = handling_user_input(plaintext)
# encrypts the plaintext using the RSA public key vlaues.
ciphertext = encrypt_plaintext(plaintext_int, e, n )

# REFERENCE: The file path and file creation/writing approach was referenced from the Week 7 lectorial code, file: "rsa_padding_file.py".
# It was adapted to fit the requirements of this task.
# saves the ciphertext and the initals of the user in the output folder.
output_file = os.path.join(BASE, "output", "cipher.txt")
with open (output_file, "w") as file:
    file.write(f"{ciphertext}\n")
    file.write(f"{initials}")

# REFERENCE: The file path and file creation/writing approach was referenced from the Week 7 lectorial code, file: "rsa_padding_file.py".
# It was adapted to fit the requirements of this task.
# saves the public key values e and n in the key folder
key_file = os.path.join(BASE, "keys", "key.txt")
with open(key_file, "w") as file:
    file.write(f"({e}, {n})")
    
            






    

