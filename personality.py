"""
Personality Analyzer - Determines crypto personality type based on user behavior
"""
import json
import random
from typing import Dict, Any, List, Optional
from pathlib import Path

class PersonalityAnalyzer:
    def __init__(self):
        self.personalities = self._load_personalities()
        self.personality_list = self.personalities['personalities']
        self.compatibility_matrix = self.personalities['compatibility_matrix']
    
    def _load_personalities(self) -> Dict[str, Any]:
        """Load personality definitions from JSON"""
        personality_file = Path(__file__).parent / 'personality_profiles' / 'personalities.json'
        with open(personality_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def analyze_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze user data and determine personality type
        
        Args:
            user_data: Dictionary containing:
                - fid: Farcaster ID
                - username: Farcaster username
                - bio: User bio (optional)
                - recent_casts: Recent posts (optional)
                - nft_holdings: NFT data (optional)
                - token_holdings: Token holdings (optional)
        
        Returns:
            Dictionary with personality analysis
        """
        # Calculate personality scores based on available data
        scores = self._calculate_personality_scores(user_data)
        
        # Determine best matching personality
        personality_type = self._determine_personality(scores)
        personality_data = self._get_personality_data(personality_type)
        
        return {
            'personality_type': personality_type,
            'personality_name': personality_data['name'],
            'personality_emoji': personality_data['emoji'],
            'description': personality_data['description'],
            'scores': scores,
            'traits': personality_data['traits'],
            'comedy_lines': random.sample(personality_data['comedy_lines'], 
                                         min(2, len(personality_data['comedy_lines']))),
            'red_flags': personality_data['red_flags'][:3],
            'green_flags': personality_data['green_flags'][:3]
        }
    
    def _calculate_personality_scores(self, user_data: Dict[str, Any]) -> Dict[str, int]:
        """Calculate personality trait scores from user data"""
        scores = {
            'risk_tolerance': 50,
            'nft_interest': 50,
            'defi_engagement': 50,
            'meme_coin_tolerance': 50,
            'token_preference_btc': 30,
            'token_preference_eth': 30,
            'token_preference_alt': 40
        }
        
        # Analyze bio for keywords
        bio = user_data.get('bio', '').lower()
        if bio:
            # Bitcoin signals
            if any(word in bio for word in ['bitcoin', 'btc', 'maxi', 'sound money']):
                scores['token_preference_btc'] += 30
                scores['risk_tolerance'] -= 10
            
            # Ethereum signals
            if any(word in bio for word in ['ethereum', 'eth', 'defi', 'smart contract']):
                scores['token_preference_eth'] += 30
                scores['defi_engagement'] += 20
            
            # NFT signals
            if any(word in bio for word in ['nft', 'pfp', 'art', 'collector', 'opensea']):
                scores['nft_interest'] += 30
            
            # Meme/shitcoin signals
            if any(word in bio for word in ['degen', 'ape', 'moon', 'lambo', 'meme']):
                scores['meme_coin_tolerance'] += 30
                scores['risk_tolerance'] += 20
            
            # Conservative signals
            if any(word in bio for word in ['hodl', 'long term', 'investor', 'stable']):
                scores['risk_tolerance'] -= 15
        
        # Analyze recent casts
        recent_casts = user_data.get('recent_casts', [])
        if recent_casts:
            cast_text = ' '.join([cast.get('text', '').lower() for cast in recent_casts[:20]])
            
            # Count mentions
            btc_mentions = cast_text.count('btc') + cast_text.count('bitcoin')
            eth_mentions = cast_text.count('eth') + cast_text.count('ethereum')
            nft_mentions = cast_text.count('nft')
            defi_mentions = cast_text.count('defi') + cast_text.count('yield')
            
            if btc_mentions > eth_mentions * 2:
                scores['token_preference_btc'] += 20
            elif eth_mentions > btc_mentions * 2:
                scores['token_preference_eth'] += 20
            
            if nft_mentions > 5:
                scores['nft_interest'] += 20
            
            if defi_mentions > 5:
                scores['defi_engagement'] += 20
        
        # Analyze NFT holdings
        nft_holdings = user_data.get('nft_holdings', [])
        if nft_holdings:
            nft_count = len(nft_holdings)
            if nft_count > 10:
                scores['nft_interest'] = min(95, scores['nft_interest'] + 30)
            elif nft_count > 3:
                scores['nft_interest'] = min(90, scores['nft_interest'] + 20)
        
        # Analyze token holdings
        token_holdings = user_data.get('token_holdings', {})
        if token_holdings:
            # Check for diverse holdings (more tokens = more risk-tolerant)
            token_count = len(token_holdings)
            if token_count > 10:
                scores['risk_tolerance'] = min(95, scores['risk_tolerance'] + 20)
                scores['meme_coin_tolerance'] = min(90, scores['meme_coin_tolerance'] + 20)
            
            # Check for specific tokens
            if 'BTC' in token_holdings or 'WBTC' in token_holdings:
                scores['token_preference_btc'] += 15
            if 'ETH' in token_holdings:
                scores['token_preference_eth'] += 15
        
        # Normalize scores to 0-100 range
        for key in scores:
            scores[key] = max(0, min(100, scores[key]))
        
        return scores
    
    def _determine_personality(self, scores: Dict[str, int]) -> str:
        """Determine personality type from scores"""
        # Calculate match score for each personality type
        personality_matches = []
        
        for personality in self.personality_list:
            traits = personality['traits']
            match_score = 0
            
            # Compare risk tolerance
            risk_diff = abs(traits['risk_tolerance'] - scores['risk_tolerance'])
            match_score += (100 - risk_diff) * 0.25
            
            # Compare NFT interest
            nft_diff = abs(traits['nft_interest'] - scores['nft_interest'])
            match_score += (100 - nft_diff) * 0.20
            
            # Compare DeFi engagement
            defi_diff = abs(traits['defi_engagement'] - scores['defi_engagement'])
            match_score += (100 - defi_diff) * 0.25
            
            # Compare meme coin tolerance
            meme_diff = abs(traits['meme_coin_tolerance'] - scores['meme_coin_tolerance'])
            match_score += (100 - meme_diff) * 0.20
            
            # Token preference bonus
            if traits['token_preference'] == 'btc_only' and scores['token_preference_btc'] > 70:
                match_score += 10
            elif traits['token_preference'] == 'eth_ecosystem' and scores['token_preference_eth'] > 70:
                match_score += 10
            
            personality_matches.append({
                'id': personality['id'],
                'score': match_score
            })
        
        # Return personality with highest match score
        best_match = max(personality_matches, key=lambda x: x['score'])
        return best_match['id']
    
    def _get_personality_data(self, personality_id: str) -> Dict[str, Any]:
        """Get personality data by ID"""
        for personality in self.personality_list:
            if personality['id'] == personality_id:
                return personality
        return self.personality_list[0]  # Default fallback
    
    def calculate_compatibility(self, personality1: str, personality2: str) -> int:
        """Calculate compatibility score between two personality types"""
        if personality1 in self.compatibility_matrix:
            if personality2 in self.compatibility_matrix[personality1]:
                return self.compatibility_matrix[personality1][personality2]
        
        # Fallback: calculate based on trait similarity
        p1_data = self._get_personality_data(personality1)
        p2_data = self._get_personality_data(personality2)
        
        if not p1_data or not p2_data:
            return 50
        
        t1 = p1_data['traits']
        t2 = p2_data['traits']
        
        # Calculate similarity
        risk_sim = 100 - abs(t1['risk_tolerance'] - t2['risk_tolerance'])
        nft_sim = 100 - abs(t1['nft_interest'] - t2['nft_interest'])
        defi_sim = 100 - abs(t1['defi_engagement'] - t2['defi_engagement'])
        meme_sim = 100 - abs(t1['meme_coin_tolerance'] - t2['meme_coin_tolerance'])
        
        compatibility = (risk_sim * 0.3 + nft_sim * 0.25 + defi_sim * 0.25 + meme_sim * 0.2)
        return int(compatibility)
    
    def get_all_personalities(self) -> List[Dict[str, Any]]:
        """Get list of all available personality types"""
        return [{
            'id': p['id'],
            'name': p['name'],
            'emoji': p['emoji'],
            'description': p['description']
        } for p in self.personality_list]
    
    def get_personality_by_id(self, personality_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed personality data by ID"""
        return self._get_personality_data(personality_id)
