import os
import sys
from sqlalchemy.orm import Session
import uuid
from dotenv import load_dotenv

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal, engine
from app.models.user import User
from app.core.auth import get_password_hash

# Load environment variables
load_dotenv()

def create_test_user():
    """Create a test user in the database"""
    db = SessionLocal()
    
    try:
        # Check if test user already exists
        test_user = db.query(User).filter(User.email == "test@example.com").first()
        
        if test_user:
            print(f"Test user already exists: {test_user.email}")
            return
        
        # Create new test user
        new_user = User(
            id=str(uuid.uuid4()),
            email="test@example.com",
            hashed_password=get_password_hash("password123"),
            first_name="Test",
            last_name="User",
            is_active=True,
            is_verified=True,
            subscription_tier="basic",
            minutes_remaining=60
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print(f"Test user created successfully: {new_user.email}")
        print(f"Password: password123")
        
    except Exception as e:
        print(f"Error creating test user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user() 