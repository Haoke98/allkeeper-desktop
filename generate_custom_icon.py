import os
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont

# Define paths
BASE_DIR = os.getcwd()
ICONSET_DIR = os.path.join(BASE_DIR, 'MyIcon.iconset')
ICNS_OUTPUT = os.path.join(BASE_DIR, 'allkeeper.icns')
ICO_OUTPUT = os.path.join(BASE_DIR, 'allkeeper.ico')

def draw_icon(size):
    # macOS Big Sur style rounded rectangle
    # Background Color: Dark Blue (Technology/Security)
    bg_color = (13, 37, 56)  # #0D2538 (Deep Navy)
    # Accent Color: Bright Blue
    accent_color = (0, 122, 255) # #007AFF (Apple Blue)
    white = (255, 255, 255)
    
    # Create base image with transparency
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 1. Background: Rounded Rectangle (Squircle-ish)
    # For macOS, the system usually handles the masking, but providing a rounded rect is good practice
    # Actually, for ICNS, full bleed square is often masked by OS, but let's make it look nice
    # Let's draw a rounded rectangle covering most of the area
    padding = size // 10
    rect_coords = [padding, padding, size - padding, size - padding]
    radius = size // 5
    draw.rounded_rectangle(rect_coords, radius=radius, fill=bg_color)
    
    # 2. Draw a Shield Outline (Symbolizing "Keeper")
    # Shield shape: Top flat/curved, bottom point
    shield_w = size * 0.5
    shield_h = size * 0.6
    center_x = size // 2
    center_y = size // 2
    
    # Shield coordinates
    # Top left, Top Right, Bottom Point
    # Using a simple path for shield
    shield_top_y = center_y - shield_h // 2
    shield_bottom_y = center_y + shield_h // 2
    shield_left_x = center_x - shield_w // 2
    shield_right_x = center_x + shield_w // 2
    
    # Bezier-like curve points for shield bottom
    # (x0, y0), (x1, y1), ...
    # Simplified shield:
    # 1. Top Edge (straight or slightly curved down)
    # 2. Side Edges (straight down for a bit)
    # 3. Bottom Curves meeting at point
    
    points = [
        (shield_left_x, shield_top_y), # Top Left
        (shield_right_x, shield_top_y), # Top Right
        (shield_right_x, center_y), # Mid Right
        (center_x, shield_bottom_y), # Bottom Point
        (shield_left_x, center_y), # Mid Left
    ]
    
    # Draw Shield Fill
    draw.polygon(points, fill=accent_color)
    
    # 3. Draw "Server" lines inside the Shield (Symbolizing "Server/Jump")
    # Three horizontal lines
    line_w = shield_w * 0.6
    line_h = shield_h * 0.1
    line_gap = line_h * 0.8
    
    start_y = shield_top_y + (shield_h * 0.25)
    
    for i in range(3):
        ly = start_y + i * (line_h + line_gap)
        lx1 = center_x - line_w // 2
        lx2 = center_x + line_w // 2
        ly2 = ly + line_h
        
        draw.rounded_rectangle([lx1, ly, lx2, ly2], radius=line_h//2, fill=white)
        
        # Add a small "LED" dot on the right of each server line
        led_size = line_h * 0.6
        led_x = lx2 - line_h 
        led_y = ly + (line_h - led_size) // 2
        draw.ellipse([led_x, led_y, led_x + led_size, led_y + led_size], fill=(0, 255, 0)) # Green LED

    return img

def generate_icons():
    print("Generating custom icons...")
    
    # Generate ICNS (macOS)
    if os.path.exists(ICONSET_DIR):
        shutil.rmtree(ICONSET_DIR)
    os.makedirs(ICONSET_DIR)

    # Sizes for iconset
    sizes = [16, 32, 128, 256, 512]
    
    # For ICO, we'll keep the largest one
    max_img = None
    
    try:
        for size in sizes:
            # Normal
            img = draw_icon(size)
            img.save(os.path.join(ICONSET_DIR, f'icon_{size}x{size}.png'))
            
            # Retina (@2x)
            double_size = size * 2
            img_2x = draw_icon(double_size)
            img_2x.save(os.path.join(ICONSET_DIR, f'icon_{size}x{size}@2x.png'))
            
            if size == 512: # actually use 1024 (512@2x) for high res ICO
                max_img = img_2x

        # Create .icns
        cmd = ['iconutil', '-c', 'icns', ICONSET_DIR, '-o', ICNS_OUTPUT]
        subprocess.run(cmd, check=True)
        print(f"Created {ICNS_OUTPUT}")
        
        # Create .ico
        # Windows sizes: 16, 32, 48, 64, 128, 256
        ico_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        ico_imgs = []
        for w, h in ico_sizes:
            ico_imgs.append(draw_icon(w)) # Re-draw for specific sizes to look crisp
            
        ico_imgs[0].save(ICO_OUTPUT, format='ICO', sizes=ico_sizes, append_images=ico_imgs[1:])
        print(f"Created {ICO_OUTPUT}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if os.path.exists(ICONSET_DIR):
            shutil.rmtree(ICONSET_DIR)

if __name__ == "__main__":
    generate_icons()
