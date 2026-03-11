from exceptions import UserNotFoundError, InvalidPasswordError
from models import User
from models.password_body import PasswordUpdateRequest
from core.seciurity import bcrypt_context


class UserSettingsService:
    def __init__(self, db):
        self.db = db

    def get_user_info(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()

        if user is None:
            raise UserNotFoundError()

        return {"first_name": user.first_name, "email": user.email, "role": user.role}

    def update_password(self, user_id: int, password_request: PasswordUpdateRequest):
        user = self.db.query(User).filter(User.id == user_id).first()

        if user is None:
            raise UserNotFoundError()

        password_verification = bcrypt_context.verify(password_request.current_password, user.hashed_password)

        if not password_verification:
            raise InvalidPasswordError()

        user.hashed_password = bcrypt_context.hash(password_request.new_password)

        self.db.commit()

        return {"message": "Password updated successfully"}




