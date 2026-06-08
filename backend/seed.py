import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from app.database.postgres import SessionLocal
from app.models.user_model import User
from app.auth.security import hash_password
from app.models.role_enum import Role

def seed():
    db = SessionLocal()
    
    # User 1: ashok@gmail.com
    email1 = 'ashok@gmail.com'
    existing1 = db.query(User).filter(User.email == email1).first()
    if not existing1:
        user1 = User(
            name='Ashok',
            email=email1,
            password=hash_password('admin'),
            role=Role.ADMIN
        )
        db.add(user1)
        print(f'Created user {email1}')
    else:
        existing1.password = hash_password('admin')
        existing1.role = Role.ADMIN
        print(f'Updated user {email1}')

    # User 2: kirthiga@gmail.com
    email2 = 'kirthiga@gmail.com'
    existing2 = db.query(User).filter(User.email == email2).first()
    if not existing2:
        user2 = User(
            name='Kirthiga',
            email=email2,
            password=hash_password('12345'),
            role=Role.ADMIN
        )
        db.add(user2)
        print(f'Created user {email2}')
    else:
        existing2.password = hash_password('12345')
        existing2.role = Role.ADMIN
        print(f'Updated user {email2}')

    db.commit()

if __name__ == "__main__":
    seed()
