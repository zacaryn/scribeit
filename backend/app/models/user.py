from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func
import uuid
from ..db.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Subscription details
    stripe_customer_id = Column(String, nullable=True)
    subscription_tier = Column(String, default="free")  # free, basic, pro
    subscription_status = Column(String, default="active")  # active, inactive, trial
    minutes_used = Column(Float, default=0)
    minutes_remaining = Column(Float, default=30)  # Start with 30 free minutes
    subscription_renewal_date = Column(DateTime(timezone=True), nullable=True) 