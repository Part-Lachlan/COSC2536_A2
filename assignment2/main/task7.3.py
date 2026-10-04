import os
import random
import Crypto.Util.number
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
# Prompts the user to enter their first and last namee, if input is invalid it repormmpts them. Then it extracts the intials from the first and last name and captialises them.
full_name = handling_first_and_last_name()
first_name, last_name = full_name.split()
initials = (first_name[0] + last_name[0]).upper()


print("Your initials are: ", initials)

Prime_1 = input("Enter a prime number between  1000000000 and 9999999999:")


    

