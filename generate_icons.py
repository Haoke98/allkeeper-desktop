import os
import shutil
import subprocess
from PIL import Image

# Define paths
BASE_DIR = os.getcwd()
# Try logo-sdm.png first as it might be the square version without text
LOGO_PATH = os.path.join(BASE_DIR, 'service/common-static/img/logo-sdm.png')
# LOGO_PATH = os.path.join(BASE_DIR, 'service/common-static/img/LOGO.png')
# Use temp dir for iconset
ICONSET_DIR = os.path.join(BASE_DIR, 'MyIcon.iconset')
ICNS_OUTPUT = os.path.join(BASE_DIR, 'allkeeper.icns')
ICO_OUTPUT = os.path.join(BASE_DIR, 'allkeeper.ico')

def generate_icns():
    print(f"Generating .icns file from {LOGO_PATH}...")
    if not os.path.exists(LOGO_PATH):
        print(f"Error: Logo file not found at {LOGO_PATH}")
        return

    if os.path.exists(ICONSET_DIR):
        shutil.rmtree(ICONSET_DIR)
    os.makedirs(ICONSET_DIR)

    # Sizes required for iconset
    # format: icon_{size}x{size}.png and icon_{size}x{size}@2x.png
    # 16, 32, 128, 256, 512
    sizes = [16, 32, 128, 256, 512]
    
    try:
        with Image.open(LOGO_PATH) as img:
            for size in sizes:
                # Normal size
                resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
                resized_img.save(os.path.join(ICONSET_DIR, f'icon_{size}x{size}.png'))
                
                # @2x size
                double_size = size * 2
                resized_double = img.resize((double_size, double_size), Image.Resampling.LANCZOS)
                resized_double.save(os.path.join(ICONSET_DIR, f'icon_{size}x{size}@2x.png'))

        # Use iconutil to create .icns
        # iconutil -c icns MyIcon.iconset -o allkeeper.icns
        cmd = ['iconutil', '-c', 'icns', ICONSET_DIR, '-o', ICNS_OUTPUT]
        print(f"Running command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        print(f"Successfully created {ICNS_OUTPUT}")
        
    except Exception as e:
        print(f"Error generating ICNS: {e}")
    finally:
        # Cleanup
        if os.path.exists(ICONSET_DIR):
            shutil.rmtree(ICONSET_DIR)

def generate_ico():
    print("Generating .ico file...")
    if not os.path.exists(LOGO_PATH):
        print(f"Error: Logo file not found at {LOGO_PATH}")
        return

    try:
        with Image.open(LOGO_PATH) as img:
            # Save as ICO, including multiple sizes
            # Windows uses 16, 32, 48, 64, 128, 256
            img.save(ICO_OUTPUT, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
            print(f"Successfully created {ICO_OUTPUT}")
    except Exception as e:
        print(f"Error generating ICO: {e}")

if __name__ == "__main__":
    generate_icns()
    generate_ico()
