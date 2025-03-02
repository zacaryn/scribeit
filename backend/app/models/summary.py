from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from ..db.database import Base

class Summary(Base):
    __tablename__ = "summaries"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=True)
    source_type = Column(String, nullable=False)  # "file_upload", "youtube", etc.
    original_filename = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    s3_file_key = Column(String, nullable=True)
    duration_seconds = Column(Float, nullable=True)
    minutes_charged = Column(Float, nullable=True)
    
    # Processing status
    status = Column(String, default="pending")  # pending, processing, completed, failed
    error_message = Column(String, nullable=True)
    
    # Content
    transcription = Column(Text, nullable=True)
    summary_text = Column(Text, nullable=True)
    key_points = Column(JSON, nullable=True)  # Store as JSON array
    action_items = Column(JSON, nullable=True)  # Store as JSON array
    speaker_labels = Column(JSON, nullable=True)  # Store as JSON object mapping speaker ids to text
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", backref="summaries") 