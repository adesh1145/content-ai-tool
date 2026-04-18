import hashlib
import bcrypt

from app.features.auth.domain.model.hashed_password import HashedPassword


class PasswordService:
    """Domain service for password hashing and verification."""

    @staticmethod
    def _pre_hash(raw_password: str) -> bytes:
        """Pre-hash with SHA-256 to bypass bcrypt's 72-byte limit securely."""
        return hashlib.sha256(raw_password.encode('utf-8')).hexdigest().encode('utf-8')

    @staticmethod
    def hash(raw_password: str) -> HashedPassword:
        # Pre-hash and then explicitly hash with bcrypt natively
        hashed_bytes = bcrypt.hashpw(PasswordService._pre_hash(raw_password), bcrypt.gensalt())
        return HashedPassword(hashed_bytes.decode('utf-8'))

    @staticmethod
    def verify(raw_password: str, hashed: HashedPassword) -> bool:
        try:
            return bcrypt.checkpw(
                PasswordService._pre_hash(raw_password),
                hashed.value.encode('utf-8')
            )
        except ValueError:
            return False
