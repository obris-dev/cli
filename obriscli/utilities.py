import string
import secrets


def make_id(id_len, case_sensitive=True):
    alphabet = string.ascii_letters + string.digits
    uniq_id = ''.join(secrets.choice(alphabet) for i in range(id_len))

    if case_sensitive:
        return uniq_id
    return uniq_id.lower()
