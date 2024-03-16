from db.config import new_session
from db.models import UserORM

class UserCRUD:
    def create_user(self, user):
        with new_session() as session:
            new_user = UserORM(**user.dict())
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user