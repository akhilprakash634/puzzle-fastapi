from typing import Optional
from app.core.security import get_password_hash, verify_password
from app.schemas.user import UserCreate, UserInDB, User
from app.core.firebase import db

class CRUDUser:
    def get(self, id: str) -> Optional[User]:
        doc = db.collection("users").document(id).get()
        if doc.exists:
            user_data = doc.to_dict()
            return User(id=doc.id, **user_data)
        return None

    def get_by_email(self, email: str) -> Optional[UserInDB]:
        users = db.collection("users").where("email", "==", email).limit(1).get()
        for user in users:
            user_data = user.to_dict()
            return UserInDB(id=user.id, **user_data)
        return None

    def create(self, obj_in: UserCreate) -> User:
        hashed_password = get_password_hash(obj_in.password)
        user_data = obj_in.dict(exclude={"password"})
        user_data["hashed_password"] = hashed_password
        doc_ref = db.collection("users").document()
        doc_ref.set(user_data)
        return User(id=doc_ref.id, **user_data)

    def authenticate(self, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return User(
            id=user.id,
            email=user.email,
            name=user.name,
            phone_number=user.phone_number,
            age=user.age
        )

user = CRUDUser()