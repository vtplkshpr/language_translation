"""
Database service for language translation
"""
import logging
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from models.translation_models import Base
from utils.config import config

logger = logging.getLogger(__name__)

class DatabaseService:
    """Database service for translation models"""
    
    def __init__(self):
        self.engine = None
        self.session_factory = None
        self._setup_database()
    
    def _setup_database(self):
        """Setup database connection"""
        try:
            if not config.DATABASE_URL:
                logger.error("DATABASE_URL not configured")
                return
            
            # Convert sync URL to async if needed
            database_url = config.DATABASE_URL
            if database_url.startswith('postgresql://'):
                database_url = database_url.replace('postgresql://', 'postgresql+asyncpg://', 1)
            
            self.engine = create_async_engine(
                database_url,
                echo=False,
                pool_pre_ping=True,
                pool_recycle=3600
            )
            
            self.session_factory = async_sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            
            logger.info("Database service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to setup database: {e}")
    
    @asynccontextmanager
    async def get_session(self):
        """Get database session"""
        if not self.session_factory:
            raise RuntimeError("Database not initialized")
        
        async with self.session_factory() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                logger.error(f"Database session error: {e}")
                raise
            finally:
                await session.close()
    
    async def create_tables(self):
        """Create all tables"""
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
    
    async def test_connection(self) -> bool:
        """Test database connection"""
        try:
            async with self.get_session() as session:
                from sqlalchemy import text
                await session.execute(text("SELECT 1"))
            logger.info("Database connection test successful")
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    async def close(self):
        """Close database connection"""
        if self.engine:
            await self.engine.dispose()
            logger.info("Database connection closed")

# Global database service instance
db_service = DatabaseService()
