# pylint: skip-file

from hashlib import pbkdf2_hmac


def get_ticket(nodename, ticketsalt):
    iterations = 50000

    byte_string = nodename.encode()
    salt = ticketsalt.encode()

    password_hash = pbkdf2_hmac('sha1', byte_string, salt, iterations, dklen=20).hex()
    return password_hash


class FilterModule(object):
    def filters(self):
        return {
            "icinga2_ticket": get_ticket,
        }
