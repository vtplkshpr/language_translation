#!/usr/bin/env python3
"""
Initialize database for language translation ability
"""
import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
# Try to load from multiple locations
load_dotenv()  # Current directory
load_dotenv('.env')  # Explicit .env file
load_dotenv('../.env')  # Parent directory
load_dotenv('../../.env')  # Root directory

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from services.database import DatabaseService
from utils.config import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_database():
    """Initialize database tables for language translation"""
    try:
        logger.info("Initializing database for language_translation...")
        
        # Create database service
        db_service = DatabaseService()
        
        # Test connection first
        if not await db_service.test_connection():
            logger.error("Database connection failed. Please check your DATABASE_URL configuration.")
            return False
        
        logger.info("Database connection successful!")
        
        # Create tables
        await db_service.create_tables()
        logger.info("Database tables created successfully!")
        
        # Close connection
        await db_service.close()
        
        logger.info("Database initialization completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False

async def main():
    """Main function"""
    print("🗄️  Initializing Language Translation Database...")
    print("=" * 50)
    
    # Check if DATABASE_URL is configured
    if not config.DATABASE_URL:
        print("❌ DATABASE_URL not configured!")
        print("Please set DATABASE_URL in your .env file or environment variables.")
        return False
    
    print(f"📊 Database URL: {config.DATABASE_URL}")
    print()
    
    success = await init_database()
    
    if success:
        print("\n✅ Database initialization completed successfully!")
        print("You can now use the language translation service.")
    else:
        print("\n❌ Database initialization failed!")
        print("Please check your database configuration and try again.")
    
    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
