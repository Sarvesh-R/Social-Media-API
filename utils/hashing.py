import bcrypt

# --------------------------------------------------------
# VERIFY PLAIN PASSWORD AGAINST HASHED PASSWORD
# --------------------------------------------------------
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

# --------------------------------------------------------
# HASH A PLAIN PASSWORD USING BCRYPT
# --------------------------------------------------------
def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
