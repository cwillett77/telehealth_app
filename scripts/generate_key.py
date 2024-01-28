import string
import random

chars = string.ascii_letters + string.digits + string.punctuation
secret_key = ''.join(random.choice(chars) for _ in range(50))
print(secret_key)