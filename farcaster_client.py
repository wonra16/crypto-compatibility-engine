"""
Farcaster Integration - Fetch user data and social graph
"""
import os
import httpx
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

class FarcasterClient:
    def __init__(self):
        self.api_key = os.getenv('FARCASTER_API_KEY')
        self.base_url = "https://api.neynar.com/v2"
        self.headers = {
            "accept": "application/json",
            "api_key": self.api_key
        } if self.api_key else {}
        
    async def get_user_by_fid(self, fid: int) -> Optional[Dict[str, Any]]:
        """Get user information by FID"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/farcaster/user/bulk",
                    params={"fids": str(fid)},
                    headers=self.headers,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    users = data.get('users', [])
                    if users:
                        return self._format_user_data(users[0])
                return None
                
        except Exception as e:
            print(f"Error fetching user {fid}: {e}")
            return None
    
    async def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user information by username"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/farcaster/user/search",
                    params={"q": username},
                    headers=self.headers,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    users = data.get('result', {}).get('users', [])
                    if users:
                        return self._format_user_data(users[0])
                return None
                
        except Exception as e:
            print(f"Error fetching user {username}: {e}")
            return None
    
    async def get_user_casts(self, fid: int, limit: int = 25) -> List[Dict[str, Any]]:
        """Get recent casts from a user"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/farcaster/feed/user/{fid}",
                    params={"limit": limit},
                    headers=self.headers,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    casts = data.get('casts', [])
                    return [self._format_cast_data(cast) for cast in casts]
                return []
                
        except Exception as e:
            print(f"Error fetching casts for {fid}: {e}")
            return []
    
    async def get_user_followers(self, fid: int, limit: int = 100) -> List[int]:
        """Get list of user's followers (FIDs)"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/farcaster/followers",
                    params={"fid": fid, "limit": limit},
                    headers=self.headers,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    users = data.get('users', [])
                    return [user.get('fid') for user in users if user.get('fid')]
                return []
                
        except Exception as e:
            print(f"Error fetching followers for {fid}: {e}")
            return []
    
    async def get_user_following(self, fid: int, limit: int = 100) -> List[int]:
        """Get list of users that this user follows (FIDs)"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/farcaster/following",
                    params={"fid": fid, "limit": limit},
                    headers=self.headers,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    users = data.get('users', [])
                    return [user.get('fid') for user in users if user.get('fid')]
                return []
                
        except Exception as e:
            print(f"Error fetching following for {fid}: {e}")
            return []
    
    async def get_mutual_connections(self, fid: int) -> List[int]:
        """Get users that both follow each other"""
        try:
            followers = await self.get_user_followers(fid)
            following = await self.get_user_following(fid)
            
            # Find mutual connections
            mutuals = list(set(followers) & set(following))
            return mutuals
            
        except Exception as e:
            print(f"Error getting mutual connections for {fid}: {e}")
            return []
    
    async def get_social_graph_connections(self, fid: int, depth: int = 2) -> List[int]:
        """
        Get connections from social graph
        depth=1: direct following
        depth=2: following + their following
        """
        try:
            connections = set()
            
            # Get direct following
            following = await self.get_user_following(fid, limit=150)
            connections.update(following)
            
            if depth >= 2 and following:
                # Get second-degree connections (sample to avoid rate limits)
                sample_size = min(10, len(following))
                import random
                sampled_following = random.sample(following, sample_size)
                
                for friend_fid in sampled_following:
                    friend_following = await self.get_user_following(friend_fid, limit=50)
                    connections.update(friend_following)
            
            # Remove self
            connections.discard(fid)
            
            return list(connections)
            
        except Exception as e:
            print(f"Error getting social graph for {fid}: {e}")
            return []
    
    def _format_user_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format raw API user data"""
        profile = raw_data.get('profile', {})
        
        return {
            'fid': raw_data.get('fid'),
            'username': raw_data.get('username'),
            'display_name': raw_data.get('display_name'),
            'bio': profile.get('bio', {}).get('text', ''),
            'pfp_url': raw_data.get('pfp_url'),
            'follower_count': raw_data.get('follower_count', 0),
            'following_count': raw_data.get('following_count', 0),
            'verified_addresses': raw_data.get('verified_addresses', {})
        }
    
    def _format_cast_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format raw API cast data"""
        return {
            'hash': raw_data.get('hash'),
            'text': raw_data.get('text', ''),
            'timestamp': raw_data.get('timestamp'),
            'replies_count': raw_data.get('replies', {}).get('count', 0),
            'reactions_count': raw_data.get('reactions', {}).get('likes_count', 0),
            'recasts_count': raw_data.get('reactions', {}).get('recasts_count', 0)
        }
    
    async def get_comprehensive_user_data(self, fid: int) -> Dict[str, Any]:
        """Get all user data needed for personality analysis"""
        user_data = await self.get_user_by_fid(fid)
        
        if not user_data:
            return None
        
        # Get additional data
        recent_casts = await self.get_user_casts(fid, limit=25)
        
        # Combine all data
        user_data['recent_casts'] = recent_casts
        
        # You can add NFT and token holdings here if you have those APIs
        # user_data['nft_holdings'] = await self.get_nft_holdings(user_data['verified_addresses'])
        # user_data['token_holdings'] = await self.get_token_holdings(user_data['verified_addresses'])
        
        return user_data

# Mock data generator for testing without API
class MockFarcasterClient(FarcasterClient):
    """Mock client for testing without real API access"""
    
    async def get_user_by_fid(self, fid: int) -> Optional[Dict[str, Any]]:
        """Return mock user data"""
        usernames = ['cryptoking', 'degen_hunter', 'nft_lover', 'btc_maxi', 'eth_bull']
        bios = [
            'Bitcoin maxi. HODL forever. Not your keys, not your coins.',
            'DeFi degen | Yield farmer | 🌾 APY hunter',
            'NFT collector | Art enthusiast | OpenSea whale 🎨',
            'Shitcoin surfer | Moon or bust | 🚀',
            'ETH believer | Smart contracts are the future ♦️'
        ]
        
        return {
            'fid': fid,
            'username': f'{usernames[fid % len(usernames)]}_{fid}',
            'display_name': f'User {fid}',
            'bio': bios[fid % len(bios)],
            'pfp_url': f'https://i.pravatar.cc/150?u={fid}',
            'follower_count': 100 + (fid * 10) % 1000,
            'following_count': 50 + (fid * 5) % 500,
            'verified_addresses': {}
        }
    
    async def get_user_casts(self, fid: int, limit: int = 25) -> List[Dict[str, Any]]:
        """Return mock casts"""
        cast_templates = [
            "Just aped into another gem! 🚀",
            "ETH to the moon! 🌙",
            "This NFT collection is fire 🔥",
            "DeFi yields looking juicy today 🌾",
            "Bitcoin is digital gold ₿",
            "GM crypto fam! ☀️"
        ]
        
        return [{
            'hash': f'0x{fid}{i}',
            'text': cast_templates[i % len(cast_templates)],
            'timestamp': f'2024-01-{i+1:02d}',
            'replies_count': i * 2,
            'reactions_count': i * 5,
            'recasts_count': i
        } for i in range(min(limit, 10))]
    
    async def get_social_graph_connections(self, fid: int, depth: int = 2) -> List[int]:
        """Return mock connections"""
        # Generate some random FIDs as connections
        import random
        random.seed(fid)
        num_connections = random.randint(20, 100)
        return [random.randint(1000, 9999) for _ in range(num_connections)]
