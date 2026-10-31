from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)

if __name__ == "__main__":
    h = hash_password("test123")
    print(h)
    print(verify_password("test123", h))
    print(verify_password("wrong", h))
