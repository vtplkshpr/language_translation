#!/usr/bin/env python3
"""
Recreate database tables for language translation
"""
import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from services.database import DatabaseService
from models.translation_models import Base
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def recreate_tables():
    """Recreate database tables"""
    try:
        logger.info("Recreating database tables...")
        
        # Create database service
        db_service = DatabaseService()
        
        # Test connection first
        if not await db_service.test_connection():
            logger.error("Database connection failed.")
            return False
        
        # Drop all tables
        async with db_service.get_session() as session:
            await session.execute(text("DROP TABLE IF EXISTS translation_requests CASCADE"))
            await session.execute(text("DROP TABLE IF EXISTS translation_cache CASCADE"))
            await session.execute(text("DROP TABLE IF EXISTS model_info CASCADE"))
            await session.execute(text("DROP TABLE IF EXISTS translation_sessions CASCADE"))
            await session.commit()
        
        logger.info("Old tables dropped successfully!")
        
        # Create new tables
        await db_service.create_tables()
        logger.info("New tables created successfully!")
        
        # Close connection
        await db_service.close()
        
        logger.info("Database tables recreated successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Failed to recreate tables: {e}")
        return False

async def main():
    """Main function"""
    print("🔄 Recreating Language Translation Database Tables...")
    print("=" * 60)
    
    success = await recreate_tables()
    
    if success:
        print("\n✅ Database tables recreated successfully!")
    else:
        print("\n❌ Failed to recreate database tables!")
    
    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
