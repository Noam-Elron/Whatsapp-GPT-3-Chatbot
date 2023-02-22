import hashlib

def get_number_details(data):
    # User phone number is stored in the webhooks "From" ImmutableMultiDict Key, Value pair. Returned data VALUE is in the format 'whatsapp:+972542364358' as such we'll get the phone number by splitting upon the colon. ( + still remains)
    phone_number = data.split(":")
    # After the split we take the second value as that will contain the phone number.
    #phone_number = data
    phone_number = phone_number[1]
    # Create hash using md5 hash function
    hashed_number = hash_string(phone_number)
    return hashed_number, phone_number



def hash_string(data):
    hashed = hashlib.md5(data.encode(encoding="UTF-8"))
    hashed = hashed.digest()
    return hashed
