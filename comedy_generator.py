"""
Comedy Generator - AI-powered comedy generation for match results
"""
import os
import json
import random
from typing import Dict, Any, List
from pathlib import Path
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

class ComedyGenerator:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        self.use_ai = api_key is not None and api_key.strip() != ''
        
        if self.use_ai:
            try:
                self.client = AsyncOpenAI(api_key=api_key)
                print("✅ OpenAI client initialized successfully")
            except Exception as e:
                print(f"⚠️ OpenAI client initialization failed: {e}")
                self.use_ai = False
                self.client = None
        else:
            print("ℹ️ Running without OpenAI API - using template-based comedy")
            self.client = None
        
        self.comedy_templates = self._load_comedy_templates()
    
    def _load_comedy_templates(self) -> Dict[str, Any]:
        """Load comedy templates from JSON"""
        comedy_file = Path(__file__).parent / 'comedy_templates' / 'comedy.json'
        with open(comedy_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_match_comment(self, compatibility_score: int) -> str:
        """Get a funny comment based on compatibility score"""
        if compatibility_score >= 80:
            comments = self.comedy_templates['match_comments']['high_compatibility']
        elif compatibility_score >= 50:
            comments = self.comedy_templates['match_comments']['medium_compatibility']
        else:
            comments = self.comedy_templates['match_comments']['low_compatibility']
        
        return random.choice(comments)
    
    def get_date_idea(self, personality1: Dict[str, Any], personality2: Dict[str, Any]) -> str:
        """Get a date idea based on personality types"""
        # Determine category based on personalities
        p1_traits = personality1.get('traits', {})
        p2_traits = personality2.get('traits', {})
        
        avg_defi = (p1_traits.get('defi_engagement', 0) + p2_traits.get('defi_engagement', 0)) / 2
        avg_nft = (p1_traits.get('nft_interest', 0) + p2_traits.get('nft_interest', 0)) / 2
        avg_meme = (p1_traits.get('meme_coin_tolerance', 0) + p2_traits.get('meme_coin_tolerance', 0)) / 2
        avg_risk = (p1_traits.get('risk_tolerance', 0) + p2_traits.get('risk_tolerance', 0)) / 2
        
        # Choose category
        if avg_defi > 70:
            category = 'defi_focused'
        elif avg_nft > 70:
            category = 'nft_focused'
        elif avg_meme > 70:
            category = 'meme_focused'
        elif avg_risk < 40:
            category = 'conservative_focused'
        else:
            category = 'trading_focused'
        
        ideas = self.comedy_templates['date_ideas'].get(category, 
                self.comedy_templates['date_ideas']['trading_focused'])
        return random.choice(ideas)
    
    def get_trait_comment(self, personality1: Dict[str, Any], 
                         personality2: Dict[str, Any]) -> str:
        """Get a comment about shared traits"""
        p1_traits = personality1.get('traits', {})
        p2_traits = personality2.get('traits', {})
        
        comments = []
        
        # Check for similar risk tolerance
        risk_diff = abs(p1_traits.get('risk_tolerance', 50) - 
                       p2_traits.get('risk_tolerance', 50))
        if risk_diff < 20:
            if p1_traits.get('risk_tolerance', 50) > 75:
                comments.append(self.comedy_templates['trait_comments']['both_high_risk'])
            elif p1_traits.get('risk_tolerance', 50) < 40:
                comments.append(self.comedy_templates['trait_comments']['both_low_risk'])
        else:
            comments.append(self.comedy_templates['trait_comments']['opposite_risk'])
        
        # Check for NFT interest
        if p1_traits.get('nft_interest', 50) > 70 and p2_traits.get('nft_interest', 50) > 70:
            comments.append(self.comedy_templates['trait_comments']['both_nft_lovers'])
        elif p1_traits.get('nft_interest', 50) < 30 and p2_traits.get('nft_interest', 50) < 30:
            comments.append(self.comedy_templates['trait_comments']['both_nft_haters'])
        
        # Check for DeFi engagement
        if p1_traits.get('defi_engagement', 50) > 75 and p2_traits.get('defi_engagement', 50) > 75:
            comments.append(self.comedy_templates['trait_comments']['both_defi_addicts'])
        
        # Check for meme coin tolerance
        if p1_traits.get('meme_coin_tolerance', 50) > 80 and p2_traits.get('meme_coin_tolerance', 50) > 80:
            comments.append(self.comedy_templates['trait_comments']['both_memecoin_fans'])
        
        return random.choice(comments) if comments else "You both love crypto - that's a start! 💎"
    
    def get_personality_roast(self) -> str:
        """Get a random personality roast"""
        return random.choice(self.comedy_templates['personality_roasts'])
    
    def get_result_header(self, compatibility_score: int) -> str:
        """Get result header based on score"""
        if compatibility_score >= 90:
            return self.comedy_templates['result_headers']['90_100']
        elif compatibility_score >= 75:
            return self.comedy_templates['result_headers']['75_89']
        elif compatibility_score >= 60:
            return self.comedy_templates['result_headers']['60_74']
        elif compatibility_score >= 40:
            return self.comedy_templates['result_headers']['40_59']
        elif compatibility_score >= 25:
            return self.comedy_templates['result_headers']['25_39']
        else:
            return self.comedy_templates['result_headers']['0_24']
    
    async def generate_ai_comedy(self, personality1: Dict[str, Any], 
                                personality2: Dict[str, Any],
                                compatibility_score: int) -> str:
        """Generate custom comedy using GPT-4"""
        if not self.use_ai:
            return self.get_match_comment(compatibility_score)
        
        try:
            prompt = f"""You are a witty crypto dating app comedy writer. Generate a funny, short comment (max 150 characters) about this crypto compatibility match:

Person 1: {personality1['personality_name']} - {personality1['description']}
Person 2: {personality2['personality_name']} - {personality2['description']}
Compatibility Score: {compatibility_score}%

Make it funny, use crypto slang/memes, and keep it light-hearted. Include relevant emojis."""

            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a hilarious crypto comedy writer who makes funny dating jokes using crypto culture and memes."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.9
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"AI comedy generation failed: {e}")
            return self.get_match_comment(compatibility_score)
    
    async def generate_viral_share_text(self, user_data: Dict[str, Any],
                                       match_data: Dict[str, Any],
                                       compatibility_score: int) -> str:
        """Generate viral-optimized share text"""
        template = random.choice(self.comedy_templates['viral_share_templates'])
        
        match_comment = await self.generate_ai_comedy(
            user_data,
            match_data,
            compatibility_score
        )
        
        date_idea = self.get_date_idea(user_data, match_data)
        trait_comment = self.get_trait_comment(user_data, match_data)
        
        share_text = template.format(
            username=match_data.get('username', 'someone'),
            compatibility=compatibility_score,
            funny_comment=match_comment,
            trait_comment=trait_comment,
            date_idea=date_idea,
            personality_comment=user_data.get('personality_name', 'crypto person')
        )
        
        return share_text
    
    def get_opening_line(self) -> str:
        """Get a random opening line"""
        return random.choice(self.comedy_templates['opening_lines'])
    
    async def generate_full_match_content(self, user1: Dict[str, Any],
                                         user2: Dict[str, Any],
                                         compatibility_score: int) -> Dict[str, Any]:
        """Generate complete match content with all comedy elements"""
        
        # Get all comedy elements
        header = self.get_result_header(compatibility_score)
        match_comment = await self.generate_ai_comedy(user1, user2, compatibility_score)
        date_idea = self.get_date_idea(user1, user2)
        trait_comment = self.get_trait_comment(user1, user2)
        share_text = await self.generate_viral_share_text(user1, user2, compatibility_score)
        
        # Personality descriptions with comedy
        user1_roast = random.choice(user1.get('comedy_lines', [self.get_personality_roast()]))
        user2_roast = random.choice(user2.get('comedy_lines', [self.get_personality_roast()]))
        
        return {
            'header': header,
            'compatibility_score': compatibility_score,
            'match_comment': match_comment,
            'date_idea': date_idea,
            'trait_comment': trait_comment,
            'user1_roast': user1_roast,
            'user2_roast': user2_roast,
            'share_text': share_text,
            'user1_personality': {
                'name': user1.get('personality_name'),
                'emoji': user1.get('personality_emoji'),
                'description': user1.get('description')
            },
            'user2_personality': {
                'name': user2.get('personality_name'),
                'emoji': user2.get('personality_emoji'),
                'description': user2.get('description')
            }
        }
