"""
Database models for language translation
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()

class TranslationStatus(enum.Enum):
    """Translation request status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class TranslationRequest(Base):
    """Translation request model"""
    __tablename__ = 'translation_requests'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_text = Column(Text, nullable=False)
    source_language = Column(String(10), nullable=False)
    target_language = Column(String(10), nullable=False)
    translated_text = Column(Text, nullable=True)
    model_used = Column(String(50), nullable=False)
    status = Column(String(20), default=TranslationStatus.PENDING.value)
    confidence_score = Column(Float, nullable=True)
    processing_time = Column(Float, nullable=True)  # in seconds
    error_message = Column(Text, nullable=True)
    meta_data = Column(JSON, nullable=True)  # Additional metadata
    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(DateTime, default=lambda: datetime.now(), 
                       onupdate=lambda: datetime.now())
    
    def __repr__(self):
        return f"<TranslationRequest(id={self.id}, {self.source_language}->{self.target_language}, status={self.status})>"

class TranslationCache(Base):
    """Translation cache model"""
    __tablename__ = 'translation_cache'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_text = Column(Text, nullable=False)
    source_language = Column(String(10), nullable=False)
    target_language = Column(String(10), nullable=False)
    translated_text = Column(Text, nullable=False)
    model_used = Column(String(50), nullable=False)
    confidence_score = Column(Float, nullable=True)
    hit_count = Column(Integer, default=1)
    created_at = Column(DateTime, default=lambda: datetime.now())
    last_accessed = Column(DateTime, default=lambda: datetime.now(), 
                          onupdate=lambda: datetime.now())
    
    def __repr__(self):
        return f"<TranslationCache(id={self.id}, {self.source_language}->{self.target_language})>"

class ModelInfo(Base):
    """AI model information"""
    __tablename__ = 'model_info'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String(100), nullable=False, unique=True)
    provider = Column(String(50), nullable=False)  # ollama, huggingface, etc.
    size = Column(String(20), nullable=True)
    description = Column(Text, nullable=True)
    supported_languages = Column(JSON, nullable=True)
    is_available = Column(Boolean, default=True)
    last_used = Column(DateTime, nullable=True)
    usage_count = Column(Integer, default=0)
    performance_metrics = Column(JSON, nullable=True)  # avg_time, accuracy, etc.
    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(DateTime, default=lambda: datetime.now(), 
                       onupdate=lambda: datetime.now())
    
    def __repr__(self):
        return f"<ModelInfo(id={self.id}, name={self.model_name}, provider={self.provider})>"

class TranslationSession(Base):
    """Translation session for batch translations"""
    __tablename__ = 'translation_sessions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_name = Column(String(200), nullable=True)
    total_requests = Column(Integer, default=0)
    completed_requests = Column(Integer, default=0)
    failed_requests = Column(Integer, default=0)
    status = Column(String(20), default=TranslationStatus.PENDING.value)
    model_used = Column(String(50), nullable=False)
    source_language = Column(String(10), nullable=False)
    target_language = Column(String(10), nullable=False)
    meta_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<TranslationSession(id={self.id}, name={self.session_name}, status={self.status})>"
