"""
Matchmaker AI - Intelligent matching algorithm for crypto compatibility
"""
import asyncio
from typing import Dict, Any, List, Tuple
from personality import PersonalityAnalyzer
from farcaster_client import FarcasterClient, MockFarcasterClient
from comedy_generator import ComedyGenerator
import os

class MatchmakerAI:
    def __init__(self, use_mock_data: bool = False):
        self.personality_analyzer = PersonalityAnalyzer()
        self.comedy_generator = ComedyGenerator()
        
        # Use mock client if no API key or explicitly requested
        if use_mock_data or not os.getenv('FARCASTER_API_KEY'):
            self.farcaster_client = MockFarcasterClient()
        else:
            self.farcaster_client = FarcasterClient()
    
    async def analyze_user_personality(self, fid: int) -> Dict[str, Any]:
        """Analyze user's crypto personality"""
        # Get user data from Farcaster
        user_data = await self.farcaster_client.get_comprehensive_user_data(fid)
        
        if not user_data:
            raise ValueError(f"Could not fetch data for FID {fid}")
        
        # Analyze personality
        personality_analysis = self.personality_analyzer.analyze_user(user_data)
        
        # Combine with user data
        result = {
            **user_data,
            **personality_analysis
        }
        
        return result
    
    async def find_matches(self, user_fid: int, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Find top compatible matches for a user
        
        Args:
            user_fid: User's Farcaster ID
            limit: Number of matches to return
        
        Returns:
            List of match dictionaries with compatibility scores
        """
        # Analyze user's personality
        user_analysis = await self.analyze_user_personality(user_fid)
        user_personality = user_analysis['personality_type']
        
        # Get potential matches from social graph
        potential_matches = await self.farcaster_client.get_social_graph_connections(
            user_fid, 
            depth=2
        )
        
        if not potential_matches:
            # Fallback to random users if no social connections
            potential_matches = list(range(1000, 1100))
        
        # Calculate compatibility with each potential match
        match_scores = []
        
        # Process in batches to avoid overwhelming the API
        batch_size = 20
        for i in range(0, min(len(potential_matches), 100), batch_size):
            batch = potential_matches[i:i+batch_size]
            batch_results = await asyncio.gather(
                *[self._calculate_match_score(user_analysis, match_fid) 
                  for match_fid in batch],
                return_exceptions=True
            )
            
            for result in batch_results:
                if isinstance(result, dict) and result:
                    match_scores.append(result)
        
        # Sort by compatibility score
        match_scores.sort(key=lambda x: x['compatibility_score'], reverse=True)
        
        # Get top matches
        top_matches = match_scores[:limit]
        
        # Generate comedy content for each match
        for match in top_matches:
            comedy_content = await self.comedy_generator.generate_full_match_content(
                user_analysis,
                match['match_analysis'],
                match['compatibility_score']
            )
            match['comedy_content'] = comedy_content
        
        return top_matches
    
    async def _calculate_match_score(self, user_analysis: Dict[str, Any], 
                                     match_fid: int) -> Dict[str, Any]:
        """Calculate compatibility score between user and potential match"""
        try:
            # Analyze match's personality
            match_analysis = await self.analyze_user_personality(match_fid)
            
            # Calculate base compatibility from personality matrix
            base_compatibility = self.personality_analyzer.calculate_compatibility(
                user_analysis['personality_type'],
                match_analysis['personality_type']
            )
            
            # Calculate trait-based compatibility
            trait_compatibility = self._calculate_trait_compatibility(
                user_analysis['traits'],
                match_analysis['traits']
            )
            
            # Combine scores (70% personality, 30% traits)
            final_score = int(base_compatibility * 0.7 + trait_compatibility * 0.3)
            
            return {
                'match_fid': match_fid,
                'match_username': match_analysis.get('username', f'user_{match_fid}'),
                'match_display_name': match_analysis.get('display_name', ''),
                'match_pfp_url': match_analysis.get('pfp_url', ''),
                'compatibility_score': final_score,
                'match_analysis': match_analysis,
                'breakdown': {
                    'personality_match': base_compatibility,
                    'trait_match': trait_compatibility,
                    'token_preference_match': self._compare_token_preferences(
                        user_analysis['scores'],
                        match_analysis['scores']
                    ),
                    'risk_tolerance_match': self._compare_risk_tolerance(
                        user_analysis['traits'],
                        match_analysis['traits']
                    )
                }
            }
        
        except Exception as e:
            print(f"Error calculating match score for {match_fid}: {e}")
            return None
    
    def _calculate_trait_compatibility(self, traits1: Dict[str, int], 
                                      traits2: Dict[str, int]) -> int:
        """Calculate compatibility based on trait similarity"""
        risk_diff = abs(traits1.get('risk_tolerance', 50) - 
                       traits2.get('risk_tolerance', 50))
        nft_diff = abs(traits1.get('nft_interest', 50) - 
                      traits2.get('nft_interest', 50))
        defi_diff = abs(traits1.get('defi_engagement', 50) - 
                       traits2.get('defi_engagement', 50))
        meme_diff = abs(traits1.get('meme_coin_tolerance', 50) - 
                       traits2.get('meme_coin_tolerance', 50))
        
        # Convert differences to similarity scores
        risk_sim = 100 - risk_diff
        nft_sim = 100 - nft_diff
        defi_sim = 100 - defi_diff
        meme_sim = 100 - meme_diff
        
        # Weighted average
        compatibility = (
            risk_sim * 0.25 +
            nft_sim * 0.20 +
            defi_sim * 0.25 +
            meme_sim * 0.20 +
            # Bonus for complementary traits
            self._complementary_bonus(traits1, traits2) * 0.10
        )
        
        return int(compatibility)
    
    def _complementary_bonus(self, traits1: Dict[str, int], 
                           traits2: Dict[str, int]) -> int:
        """Calculate bonus for complementary traits"""
        bonus = 50  # Base score
        
        # Complementary risk levels can be good
        risk_diff = abs(traits1.get('risk_tolerance', 50) - 
                       traits2.get('risk_tolerance', 50))
        if 20 <= risk_diff <= 40:  # Moderate difference
            bonus += 20
        
        # Both high engagement in any area is good
        if (traits1.get('defi_engagement', 0) > 70 and 
            traits2.get('defi_engagement', 0) > 70):
            bonus += 15
        
        if (traits1.get('nft_interest', 0) > 70 and 
            traits2.get('nft_interest', 0) > 70):
            bonus += 15
        
        return min(bonus, 100)
    
    def _compare_token_preferences(self, scores1: Dict[str, int], 
                                  scores2: Dict[str, int]) -> int:
        """Compare token preferences between two users"""
        btc_diff = abs(scores1.get('token_preference_btc', 0) - 
                      scores2.get('token_preference_btc', 0))
        eth_diff = abs(scores1.get('token_preference_eth', 0) - 
                      scores2.get('token_preference_eth', 0))
        
        similarity = 100 - ((btc_diff + eth_diff) / 4)
        return int(max(0, min(100, similarity)))
    
    def _compare_risk_tolerance(self, traits1: Dict[str, int], 
                               traits2: Dict[str, int]) -> int:
        """Compare risk tolerance levels"""
        diff = abs(traits1.get('risk_tolerance', 50) - 
                  traits2.get('risk_tolerance', 50))
        return int(100 - diff)
    
    async def get_match_details(self, user_fid: int, match_fid: int) -> Dict[str, Any]:
        """Get detailed compatibility analysis between two specific users"""
        user_analysis = await self.analyze_user_personality(user_fid)
        match_analysis = await self.analyze_user_personality(match_fid)
        
        match_data = await self._calculate_match_score(user_analysis, match_fid)
        
        if not match_data:
            return None
        
        # Generate full comedy content
        comedy_content = await self.comedy_generator.generate_full_match_content(
            user_analysis,
            match_analysis,
            match_data['compatibility_score']
        )
        
        match_data['comedy_content'] = comedy_content
        match_data['user_analysis'] = user_analysis
        
        return match_data
    
    async def batch_analyze_users(self, fids: List[int]) -> Dict[int, Dict[str, Any]]:
        """Analyze multiple users in parallel"""
        results = await asyncio.gather(
            *[self.analyze_user_personality(fid) for fid in fids],
            return_exceptions=True
        )
        
        return {
            fid: result for fid, result in zip(fids, results)
            if isinstance(result, dict)
        }
