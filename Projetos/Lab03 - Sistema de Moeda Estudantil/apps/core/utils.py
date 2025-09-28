import random
import string

def codigo_curto(n=8) -> str:
    alfabeto = string.ascii_uppercase + string.digits
    return "".join(random.choice(alfabeto) for _ in range(n))
