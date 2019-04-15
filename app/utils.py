#Cria Textos Randômicos para recuperação de senha
import hashlib
import string
import random

def random_key(size=5): # texto randômico com caracters
    chars = string.ascii_uppercase + string.digits
    return  ''.join(random.choice(chars) for x in range(size))

def generate_hash_key(salt, random_str_size=5): # Salt -- Para solicitar informações do usuário para garantir a veracidade para a mudança de senha(ex:email)
    random_str = random_key(random_str_size)
    text = random_str + salt
    return hashlib.sha224(text.encode('utf-8')).hexdigest()
