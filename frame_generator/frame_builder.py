"""
Frame Generator - Build Farcaster Frames v2 for interactive experience
"""
from typing import Dict, Any, List, Optional
import base64
import json

class FrameGenerator:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
    
    def generate_start_frame(self) -> Dict[str, Any]:
        """Generate initial frame to start the compatibility check"""
        return {
            "version": "next",
            "image": f"{self.base_url}/images/start.png",
            "buttons": [
                {
                    "label": "🔍 Find My Crypto Match!",
                    "action": "post",
                    "target": f"{self.base_url}/api/analyze"
                },
                {
                    "label": "ℹ️ How It Works",
                    "action": "post",
                    "target": f"{self.base_url}/api/info"
                }
            ],
            "post_url": f"{self.base_url}/api/analyze",
            "image_aspect_ratio": "1:1"
        }
    
    def generate_analyzing_frame(self, username: str) -> Dict[str, Any]:
        """Frame shown while analyzing personality"""
        return {
            "version": "next",
            "image": f"{self.base_url}/images/analyzing.png",
            "buttons": [
                {
                    "label": "⏳ Analyzing...",
                    "action": "post",
                    "target": f"{self.base_url}/api/results"
                }
            ],
            "post_url": f"{self.base_url}/api/results",
            "image_aspect_ratio": "1:1"
        }
    
    def generate_personality_result_frame(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Frame showing user's personality type"""
        personality_name = analysis.get('personality_name', 'Crypto Enthusiast')
        emoji = analysis.get('personality_emoji', '🚀')
        
        return {
            "version": "next",
            "image": f"{self.base_url}/api/generate-image/personality?data={self._encode_data(analysis)}",
            "buttons": [
                {
                    "label": f"{emoji} I'm a {personality_name}!",
                    "action": "post",
                    "target": f"{self.base_url}/api/find-matches"
                },
                {
                    "label": "🔎 Find My Matches",
                    "action": "post",
                    "target": f"{self.base_url}/api/find-matches"
                }
            ],
            "post_url": f"{self.base_url}/api/find-matches",
            "image_aspect_ratio": "1:1"
        }
    
    def generate_matches_frame(self, matches: List[Dict[str, Any]], 
                              current_index: int = 0) -> Dict[str, Any]:
        """Frame showing compatibility matches"""
        if not matches or current_index >= len(matches):
            return self.generate_no_matches_frame()
        
        match = matches[current_index]
        total_matches = len(matches)
        
        buttons = []
        
        # Previous match button (if not first)
        if current_index > 0:
            buttons.append({
                "label": "⬅️ Previous",
                "action": "post",
                "target": f"{self.base_url}/api/match/{current_index - 1}"
            })
        
        # Next match button (if not last)
        if current_index < total_matches - 1:
            buttons.append({
                "label": "➡️ Next Match",
                "action": "post",
                "target": f"{self.base_url}/api/match/{current_index + 1}"
            })
        
        # View details button
        buttons.append({
            "label": "📊 View Details",
            "action": "post",
            "target": f"{self.base_url}/api/match-details/{current_index}"
        })
        
        # Share button
        buttons.append({
            "label": "📱 Share Result",
            "action": "post",
            "target": f"{self.base_url}/api/share/{current_index}"
        })
        
        return {
            "version": "next",
            "image": f"{self.base_url}/api/generate-image/match?data={self._encode_data(match)}",
            "buttons": buttons[:4],  # Max 4 buttons
            "post_url": f"{self.base_url}/api/match/{current_index}",
            "image_aspect_ratio": "1:1"
        }
    
    def generate_match_details_frame(self, match_data: Dict[str, Any]) -> Dict[str, Any]:
        """Frame showing detailed match analysis"""
        return {
            "version": "next",
            "image": f"{self.base_url}/api/generate-image/details?data={self._encode_data(match_data)}",
            "buttons": [
                {
                    "label": "⬅️ Back to Matches",
                    "action": "post",
                    "target": f"{self.base_url}/api/matches"
                },
                {
                    "label": "📱 Share This Match",
                    "action": "post",
                    "target": f"{self.base_url}/api/share-details"
                },
                {
                    "label": "🔄 Find New Matches",
                    "action": "post",
                    "target": f"{self.base_url}/api/analyze"
                }
            ],
            "post_url": f"{self.base_url}/api/matches",
            "image_aspect_ratio": "1:1"
        }
    
    def generate_share_frame(self, share_data: Dict[str, Any]) -> Dict[str, Any]:
        """Frame optimized for sharing"""
        comedy_content = share_data.get('comedy_content', {})
        share_text = comedy_content.get('share_text', 'Found my crypto soulmate!')
        
        return {
            "version": "next",
            "image": f"{self.base_url}/api/generate-image/share?data={self._encode_data(share_data)}",
            "buttons": [
                {
                    "label": "🚀 Try It Yourself!",
                    "action": "post",
                    "target": f"{self.base_url}/api/analyze"
                },
                {
                    "label": "👀 View My Matches",
                    "action": "post",
                    "target": f"{self.base_url}/api/matches"
                }
            ],
            "post_url": f"{self.base_url}/api/analyze",
            "image_aspect_ratio": "1:1"
        }
    
    def generate_no_matches_frame(self) -> Dict[str, Any]:
        """Frame when no matches found"""
        return {
            "version": "next",
            "image": f"{self.base_url}/images/no-matches.png",
            "buttons": [
                {
                    "label": "🔄 Try Again",
                    "action": "post",
                    "target": f"{self.base_url}/api/analyze"
                },
                {
                    "label": "ℹ️ Why No Matches?",
                    "action": "post",
                    "target": f"{self.base_url}/api/info"
                }
            ],
            "post_url": f"{self.base_url}/api/analyze",
            "image_aspect_ratio": "1:1"
        }
    
    def generate_error_frame(self, error_message: str = "Something went wrong") -> Dict[str, Any]:
        """Frame for error states"""
        return {
            "version": "next",
            "image": f"{self.base_url}/images/error.png",
            "buttons": [
                {
                    "label": "🔄 Try Again",
                    "action": "post",
                    "target": f"{self.base_url}/api/analyze"
                },
                {
                    "label": "🏠 Start Over",
                    "action": "post",
                    "target": f"{self.base_url}/"
                }
            ],
            "post_url": f"{self.base_url}/api/analyze",
            "image_aspect_ratio": "1:1"
        }
    
    def generate_rate_limit_frame(self) -> Dict[str, Any]:
        """Frame shown when rate limit exceeded"""
        return {
            "version": "next",
            "image": f"{self.base_url}/images/rate-limit.png",
            "buttons": [
                {
                    "label": "⏰ Come Back Later",
                    "action": "post",
                    "target": f"{self.base_url}/"
                },
                {
                    "label": "ℹ️ Learn More",
                    "action": "post",
                    "target": f"{self.base_url}/api/info"
                }
            ],
            "post_url": f"{self.base_url}/",
            "image_aspect_ratio": "1:1"
        }
    
    def generate_info_frame(self) -> Dict[str, Any]:
        """Information frame explaining how it works"""
        return {
            "version": "next",
            "image": f"{self.base_url}/images/info.png",
            "buttons": [
                {
                    "label": "🚀 Get Started",
                    "action": "post",
                    "target": f"{self.base_url}/api/analyze"
                },
                {
                    "label": "🏠 Back to Home",
                    "action": "post",
                    "target": f"{self.base_url}/"
                }
            ],
            "post_url": f"{self.base_url}/api/analyze",
            "image_aspect_ratio": "1:1"
        }
    
    def _encode_data(self, data: Dict[str, Any]) -> str:
        """Encode data for URL transmission"""
        json_str = json.dumps(data)
        encoded = base64.urlsafe_b64encode(json_str.encode()).decode()
        return encoded
    
    def _decode_data(self, encoded: str) -> Dict[str, Any]:
        """Decode data from URL"""
        try:
            decoded = base64.urlsafe_b64decode(encoded.encode()).decode()
            return json.loads(decoded)
        except:
            return {}
    
    def generate_frame_html(self, frame_data: Dict[str, Any], 
                          title: str = "Crypto Compatibility") -> str:
        """Generate HTML with frame meta tags (Farcaster v2 format)"""
        buttons_html = ""
        for i, button in enumerate(frame_data.get('buttons', [])[:4], 1):
            buttons_html += f'    <meta property="fc:frame:button:{i}" content="{button["label"]}" />\n'
            buttons_html += f'    <meta property="fc:frame:button:{i}:action" content="{button.get("action", "post")}" />\n'
            if 'target' in button:
                buttons_html += f'    <meta property="fc:frame:button:{i}:target" content="{button["target"]}" />\n'
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    
    <!-- Farcaster Frame Meta Tags (v2) -->
    <meta property="fc:frame" content="vNext" />
    <meta property="fc:frame:image" content="{frame_data['image']}" />
    <meta property="fc:frame:image:aspect_ratio" content="{frame_data.get('image_aspect_ratio', '1:1')}" />
    <meta property="fc:frame:post_url" content="{frame_data.get('post_url', self.base_url + '/api/analyze')}" />
{buttons_html}
    
    <!-- Open Graph -->
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="Find your crypto soulmate on Farcaster! AI-powered compatibility matching." />
    <meta property="og:image" content="{frame_data['image']}" />
    <meta property="og:url" content="{self.base_url}" />
    <meta property="og:type" content="website" />
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="Find your crypto soulmate on Farcaster!" />
    <meta name="twitter:image" content="{frame_data['image']}" />
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .container {{
            max-width: 600px;
            width: 100%;
        }}
        .frame-preview {{
            background: white;
            border-radius: 16px;
            padding: 32px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            text-align: center;
        }}
        h1 {{
            font-size: 2em;
            margin-bottom: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .subtitle {{
            color: #666;
            margin-bottom: 24px;
            font-size: 1.1em;
        }}
        img {{
            max-width: 100%;
            border-radius: 12px;
            margin: 24px 0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}
        .cta {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            text-decoration: none;
            display: inline-block;
            margin-top: 16px;
            font-weight: 600;
            transition: transform 0.2s;
        }}
        .cta:hover {{
            transform: translateY(-2px);
        }}
        .note {{
            color: #999;
            font-size: 0.9em;
            margin-top: 24px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="frame-preview">
            <h1>🚀 Crypto Compatibility Engine</h1>
            <p class="subtitle">Find your crypto soulmate on Farcaster!</p>
            <img src="{frame_data['image']}" alt="Crypto Compatibility Preview" />
            <a href="https://warpcast.com" class="cta">Open in Warpcast</a>
            <p class="note">This frame is interactive in Farcaster clients</p>
        </div>
    </div>
</body>
</html>"""
        return html
