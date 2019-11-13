from project.umg import bcrypt


class PasswordHasher(object):
    rounds = 12

    @staticmethod
    def encode(password):
        return bcrypt.generate_password_hash(password, rounds=PasswordHasher.rounds).decode("utf-8")

    @staticmethod
    def verify(encoded, password):
        return bcrypt.check_password_hash(encoded, password)
