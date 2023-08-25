import bcrypt


def encrypt_pass(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def compare_pass(password, hashed_password):
    if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
        return True
    else:
        return False
