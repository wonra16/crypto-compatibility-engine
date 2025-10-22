"""
Database models and connection handling for Crypto Compatibility Engine
"""
import os
from datetime import datetime
from typing import Optional, Dict, Any
import asyncpg
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
        self.database_url = os.getenv('DATABASE_URL')
    
    async def connect(self):
        """Establish database connection pool"""
        if not self.database_url:
            raise ValueError("DATABASE_URL not set in environment variables")
        
        self.pool = await asyncpg.create_pool(
            self.database_url,
            min_size=2,
            max_size=10,
            command_timeout=60
        )
        await self.create_tables()
    
    async def disconnect(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
    
    async def create_tables(self):
        """Create all necessary database tables"""
        async with self.pool.acquire() as conn:
            # Users table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    fid BIGINT PRIMARY KEY,
                    username VARCHAR(255),
                    personality_type VARCHAR(50),
                    personality_scores JSONB,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                )
            """)
            
            # Matches table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS matches (
                    id SERIAL PRIMARY KEY,
                    user_fid BIGINT REFERENCES users(fid),
                    match_fid BIGINT REFERENCES users(fid),
                    compatibility_score INTEGER,
                    match_details JSONB,
                    created_at TIMESTAMP DEFAULT NOW(),
                    UNIQUE(user_fid, match_fid)
                )
            """)
            
            # Rate limiting table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS rate_limits (
                    fid BIGINT PRIMARY KEY,
                    request_count INTEGER DEFAULT 0,
                    last_reset TIMESTAMP DEFAULT NOW()
                )
            """)
            
            # Analytics table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS analytics (
                    id SERIAL PRIMARY KEY,
                    event_type VARCHAR(50),
                    fid BIGINT,
                    event_data JSONB,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            
            # Create indexes
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_matches_user_fid ON matches(user_fid);
                CREATE INDEX IF NOT EXISTS idx_matches_compatibility ON matches(compatibility_score DESC);
                CREATE INDEX IF NOT EXISTS idx_analytics_event_type ON analytics(event_type);
                CREATE INDEX IF NOT EXISTS idx_analytics_created_at ON analytics(created_at);
            """)
    
    async def save_user(self, fid: int, username: str, personality_type: str, 
                       personality_scores: Dict[str, Any]) -> None:
        """Save or update user personality data"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO users (fid, username, personality_type, personality_scores, updated_at)
                VALUES ($1, $2, $3, $4, NOW())
                ON CONFLICT (fid) 
                DO UPDATE SET 
                    username = EXCLUDED.username,
                    personality_type = EXCLUDED.personality_type,
                    personality_scores = EXCLUDED.personality_scores,
                    updated_at = NOW()
            """, fid, username, personality_type, personality_scores)
    
    async def get_user(self, fid: int) -> Optional[Dict[str, Any]]:
        """Get user by FID"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT * FROM users WHERE fid = $1
            """, fid)
            return dict(row) if row else None
    
    async def save_match(self, user_fid: int, match_fid: int, 
                        compatibility_score: int, match_details: Dict[str, Any]) -> None:
        """Save compatibility match"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO matches (user_fid, match_fid, compatibility_score, match_details)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (user_fid, match_fid)
                DO UPDATE SET 
                    compatibility_score = EXCLUDED.compatibility_score,
                    match_details = EXCLUDED.match_details,
                    created_at = NOW()
            """, user_fid, match_fid, compatibility_score, match_details)
    
    async def get_top_matches(self, user_fid: int, limit: int = 5) -> list:
        """Get top matches for a user"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT m.*, u.username, u.personality_type
                FROM matches m
                JOIN users u ON m.match_fid = u.fid
                WHERE m.user_fid = $1
                ORDER BY m.compatibility_score DESC
                LIMIT $2
            """, user_fid, limit)
            return [dict(row) for row in rows]
    
    async def check_rate_limit(self, fid: int, max_requests: int = 100) -> bool:
        """Check if user has exceeded rate limit"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT request_count, last_reset 
                FROM rate_limits 
                WHERE fid = $1
            """, fid)
            
            now = datetime.now()
            
            if not row:
                # First request
                await conn.execute("""
                    INSERT INTO rate_limits (fid, request_count, last_reset)
                    VALUES ($1, 1, $2)
                """, fid, now)
                return True
            
            # Check if 24 hours have passed
            time_diff = (now - row['last_reset']).total_seconds()
            if time_diff > 86400:  # 24 hours
                # Reset counter
                await conn.execute("""
                    UPDATE rate_limits 
                    SET request_count = 1, last_reset = $2
                    WHERE fid = $1
                """, fid, now)
                return True
            
            # Check if under limit
            if row['request_count'] < max_requests:
                await conn.execute("""
                    UPDATE rate_limits 
                    SET request_count = request_count + 1
                    WHERE fid = $1
                """, fid)
                return True
            
            return False
    
    async def log_analytics(self, event_type: str, fid: int, event_data: Dict[str, Any]) -> None:
        """Log analytics event"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO analytics (event_type, fid, event_data)
                VALUES ($1, $2, $3)
            """, event_type, fid, event_data)
    
    async def get_analytics_summary(self, days: int = 7) -> Dict[str, Any]:
        """Get analytics summary for past N days"""
        async with self.pool.acquire() as conn:
            # Total users
            total_users = await conn.fetchval("""
                SELECT COUNT(*) FROM users
                WHERE created_at > NOW() - INTERVAL '{} days'
            """.format(days))
            
            # Total matches
            total_matches = await conn.fetchval("""
                SELECT COUNT(*) FROM matches
                WHERE created_at > NOW() - INTERVAL '{} days'
            """.format(days))
            
            # Popular personality types
            personality_stats = await conn.fetch("""
                SELECT personality_type, COUNT(*) as count
                FROM users
                WHERE created_at > NOW() - INTERVAL '{} days'
                GROUP BY personality_type
                ORDER BY count DESC
                LIMIT 5
            """.format(days))
            
            return {
                'total_users': total_users,
                'total_matches': total_matches,
                'popular_personalities': [dict(row) for row in personality_stats]
            }

# Global database instance
db = Database()
