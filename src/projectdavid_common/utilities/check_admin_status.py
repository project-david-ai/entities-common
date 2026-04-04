# src/api/entities_api/utils/check_admin_status.py
from projectdavid_orm.projectdavid_orm.models import User as UserModel
from sqlalchemy.orm import Session


def _is_admin(user_id: str, db: Session) -> bool:
    """Return True if the user exists and has is_admin=True."""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    return bool(user and user.is_admin)
