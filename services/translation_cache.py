"""
Translation cache service
"""
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from models.translation_models import TranslationCache
from services.database import db_service
from utils.config import config

logger = logging.getLogger(__name__)

class TranslationCacheService:
    """Service for managing translation cache"""
    
    def __init__(self):
        self.memory_cache = {}
        self.cache_ttl = config.CACHE_TTL
    
    async def get_cached_translation(self, source_text: str, source_lang: str, 
                                   target_lang: str) -> Optional[Dict[str, Any]]:
        """
        Get cached translation from memory or database
        
        Args:
            source_text: Source text
            source_lang: Source language
            target_lang: Target language
        
        Returns:
            Cached translation data or None
        """
        # Check memory cache first
        cache_key = f"{source_lang}:{target_lang}:{source_text}"
        if cache_key in self.memory_cache:
            cached_data = self.memory_cache[cache_key]
            if self._is_cache_valid(cached_data):
                logger.debug(f"Memory cache hit for: {source_text[:50]}...")
                return cached_data
            else:
                # Remove expired cache
                del self.memory_cache[cache_key]
        
        # Check database cache
        try:
            async with db_service.get_session() as session:
                from sqlalchemy import select
                
                result = await session.execute(
                    select(TranslationCache).where(
                        TranslationCache.source_text == source_text,
                        TranslationCache.source_language == source_lang,
                        TranslationCache.target_language == target_lang
                    )
                )
                cache_entry = result.scalar_one_or_none()
                
                if cache_entry:
                    # Check if cache is still valid
                    if self._is_cache_valid_db(cache_entry):
                        # Update hit count and last accessed
                        cache_entry.hit_count += 1
                        cache_entry.last_accessed = datetime.now()
                        await session.commit()
                        
                        # Store in memory cache
                        cached_data = {
                            'translated_text': cache_entry.translated_text,
                            'model_used': cache_entry.model_used,
                            'confidence_score': cache_entry.confidence_score,
                            'cached_at': cache_entry.created_at,
                            'hit_count': cache_entry.hit_count
                        }
                        self.memory_cache[cache_key] = cached_data
                        
                        logger.debug(f"Database cache hit for: {source_text[:50]}...")
                        return cached_data
                    else:
                        # Remove expired cache entry
                        await session.delete(cache_entry)
                        await session.commit()
                        
        except Exception as e:
            logger.error(f"Error retrieving cached translation: {e}")
        
        return None
    
    async def cache_translation(self, source_text: str, source_lang: str, 
                              target_lang: str, translated_text: str, 
                              model_used: str, confidence_score: float = None):
        """
        Cache translation result
        
        Args:
            source_text: Source text
            source_lang: Source language
            target_lang: Target language
            translated_text: Translated text
            model_used: Model used for translation
            confidence_score: Confidence score (optional)
        """
        if not config.CACHE_ENABLED:
            return
        
        cache_key = f"{source_lang}:{target_lang}:{source_text}"
        
        # Store in memory cache
        cached_data = {
            'translated_text': translated_text,
            'model_used': model_used,
            'confidence_score': confidence_score,
            'cached_at': datetime.now(),
            'hit_count': 1
        }
        self.memory_cache[cache_key] = cached_data
        
        # Store in database cache
        try:
            async with db_service.get_session() as session:
                # Check if already exists
                from sqlalchemy import select
                
                result = await session.execute(
                    select(TranslationCache).where(
                        TranslationCache.source_text == source_text,
                        TranslationCache.source_language == source_lang,
                        TranslationCache.target_language == target_lang
                    )
                )
                existing = result.scalar_one_or_none()
                
                if not existing:
                    cache_entry = TranslationCache(
                        source_text=source_text,
                        source_language=source_lang,
                        target_language=target_lang,
                        translated_text=translated_text,
                        model_used=model_used,
                        confidence_score=confidence_score
                    )
                    session.add(cache_entry)
                    await session.commit()
                    logger.debug(f"Translation cached: {source_text[:50]}...")
                else:
                    # Update existing cache
                    existing.translated_text = translated_text
                    existing.model_used = model_used
                    existing.confidence_score = confidence_score
                    existing.last_accessed = datetime.now()
                    await session.commit()
                    
        except Exception as e:
            logger.error(f"Error caching translation: {e}")
    
    def _is_cache_valid(self, cached_data: Dict[str, Any]) -> bool:
        """Check if memory cache entry is still valid"""
        cached_at = cached_data.get('cached_at')
        if not cached_at:
            return False
        
        if isinstance(cached_at, datetime):
            return datetime.now() - cached_at < timedelta(seconds=self.cache_ttl)
        
        return False
    
    def _is_cache_valid_db(self, cache_entry: TranslationCache) -> bool:
        """Check if database cache entry is still valid"""
        if not cache_entry.created_at:
            return False
        
        return datetime.now() - cache_entry.created_at < timedelta(seconds=self.cache_ttl)
    
    async def clear_cache(self, source_lang: str = None, target_lang: str = None):
        """
        Clear cache entries
        
        Args:
            source_lang: Clear cache for specific source language (optional)
            target_lang: Clear cache for specific target language (optional)
        """
        # Clear memory cache
        if source_lang and target_lang:
            # Clear specific language pair
            keys_to_remove = [
                key for key in self.memory_cache.keys() 
                if key.startswith(f"{source_lang}:{target_lang}:")
            ]
            for key in keys_to_remove:
                del self.memory_cache[key]
        else:
            # Clear all memory cache
            self.memory_cache.clear()
        
        # Clear database cache
        try:
            async with db_service.get_session() as session:
                from sqlalchemy import delete
                
                query = delete(TranslationCache)
                if source_lang:
                    query = query.where(TranslationCache.source_language == source_lang)
                if target_lang:
                    query = query.where(TranslationCache.target_language == target_lang)
                
                result = await session.execute(query)
                await session.commit()
                
                logger.info(f"Cleared {result.rowcount} cache entries")
                
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        try:
            async with db_service.get_session() as session:
                from sqlalchemy import select, func
                
                # Get total cache entries
                total_result = await session.execute(
                    select(func.count(TranslationCache.id))
                )
                total_entries = total_result.scalar()
                
                # Get total hits
                hits_result = await session.execute(
                    select(func.sum(TranslationCache.hit_count))
                )
                total_hits = hits_result.scalar() or 0
                
                # Get memory cache size
                memory_cache_size = len(self.memory_cache)
                
                return {
                    'database_entries': total_entries,
                    'memory_entries': memory_cache_size,
                    'total_hits': total_hits,
                    'cache_ttl': self.cache_ttl
                }
                
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {
                'database_entries': 0,
                'memory_entries': len(self.memory_cache),
                'total_hits': 0,
                'cache_ttl': self.cache_ttl
            }
