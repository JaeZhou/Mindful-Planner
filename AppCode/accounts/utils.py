from django.contrib.auth.tokens import PasswordResetTokenGenerator

class PasswordGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp: int):
        return str(user.pk) + str(timestamp) + user.is_email_verified