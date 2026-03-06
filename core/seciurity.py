from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_barrer = OAuth2PasswordBearer(tokenUrl="auth/token")