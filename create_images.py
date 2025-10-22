"""
Simple placeholder image generator
Creates basic images for testing
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Create static/images directory if it doesn't exist
os.makedirs('static/images', exist_ok=True)

def create_placeholder(filename, text, size=(600, 600), bg_color='#8b5cf6', text_color='white'):
    """Create a simple placeholder image"""
    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fallback to default
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Center text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size[0] - text_width) / 2
    y = (size[1] - text_height) / 2
    
    # Add emoji/icon
    draw.text((x, y - 50), "🚀", font=font, fill=text_color)
    draw.text((x, y + 20), text, font=font, fill=text_color)
    
    # Add branding
    brand_text = "Crypto Compatibility"
    bbox = draw.textbbox((0, 0), brand_text, font=small_font)
    brand_width = bbox[2] - bbox[0]
    draw.text(((size[0] - brand_width) / 2, size[1] - 50), brand_text, font=small_font, fill=text_color)
    
    img.save(f'static/images/{filename}')
    print(f"✅ Created: static/images/{filename}")

# Create all placeholder images
print("🎨 Creating placeholder images...")

create_placeholder('start.png', 'Start Match!', bg_color='#8b5cf6')
create_placeholder('analyzing.png', 'Analyzing...', bg_color='#6366f1')
create_placeholder('no-matches.png', 'No Matches', bg_color='#ef4444')
create_placeholder('error.png', 'Error', bg_color='#dc2626')
create_placeholder('rate-limit.png', 'Rate Limited', bg_color='#f59e0b')
create_placeholder('info.png', 'How It Works', bg_color='#10b981')
create_placeholder('placeholder.png', 'Coming Soon', bg_color='#6b7280')

print("\n✨ All placeholder images created!")
print("📁 Location: static/images/")
