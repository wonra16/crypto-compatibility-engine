"""
Create Mini App specific images (icon, splash, og-image)
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_gradient_background(width, height, color1='#6366f1', color2='#ec4899'):
    """Create a gradient background"""
    # Convert hex to RGB
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    c1 = hex_to_rgb(color1)
    c2 = hex_to_rgb(color2)
    
    img = Image.new('RGB', (width, height), color=c1)
    draw = ImageDraw.Draw(img)
    
    # Create gradient
    for y in range(height):
        ratio = y / height
        r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
        g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
        b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return img

def add_text(img, text, position, font_size=60, color='white'):
    """Add text to image"""
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Get text bbox for centering
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (img.width - text_width) // 2
    y = position if isinstance(position, int) else img.height // 2
    
    draw.text((x, y), text, fill=color, font=font)

def create_app_icon():
    """Create 512x512 app icon"""
    print("📱 Creating app icon...")
    img = create_gradient_background(512, 512)
    
    # Add emoji-style elements
    draw = ImageDraw.Draw(img)
    
    # Draw heart shape
    heart_color = (255, 255, 255, 200)
    
    # Big circle (background for emoji effect)
    draw.ellipse([100, 100, 412, 412], fill=(255, 255, 255, 30))
    
    # Add text
    add_text(img, "🚀💕", (200,), 150)
    
    # Save
    os.makedirs('static/images', exist_ok=True)
    img.save('static/images/icon-512.png', 'PNG')
    print("✅ Created: static/images/icon-512.png")

def create_og_image():
    """Create 1200x630 OG/Share image"""
    print("🖼️  Creating OG image...")
    img = create_gradient_background(1200, 630)
    
    # Add text
    add_text(img, "Crypto Compatibility", (150,), 80, 'white')
    add_text(img, "Find Your Soulmate 💕", (280,), 50, 'white')
    add_text(img, "🚀 💎 🤝", (400,), 100, 'white')
    
    # Save
    img.save('static/images/og-image.png', 'PNG')
    print("✅ Created: static/images/og-image.png")

def create_splash_image():
    """Create 1200x630 splash screen"""
    print("✨ Creating splash image...")
    img = create_gradient_background(1200, 630)
    
    # Add branding
    add_text(img, "Crypto Match", (200,), 90, 'white')
    add_text(img, "🚀 Loading...", (350,), 50, 'white')
    
    # Save
    img.save('static/images/splash.png', 'PNG')
    print("✅ Created: static/images/splash.png")

if __name__ == "__main__":
    print("🎨 Creating Mini App images...\n")
    
    create_app_icon()
    create_og_image()
    create_splash_image()
    
    print("\n✨ All Mini App images created!")
    print("📁 Location: static/images/")
    print("\n🔗 Test URLs:")
    print("   - Icon: /static/images/icon-512.png")
    print("   - OG Image: /static/images/og-image.png")
    print("   - Splash: /static/images/splash.png")
