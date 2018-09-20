import hashlib


def postgres_shadow(user_pwd, user_name):
    """
    Postgres uses the following method for storing
    hashed passwords.
    
    "md5" + hashed_md5("password" + "username")
    
    :returns: string
    """
    to_be_hashed = f"{user_pwd}{user_name}"
    m = hashlib.md5()
    m.update(to_be_hashed.encode())
    return f"md5{m.hexdigest()}"
    
    
class FilterModule(object):
    def filters(self):
        return {
            "postgres_shadow": postgres_shadow,
        }

