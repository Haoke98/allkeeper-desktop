import os
import sys
import subprocess
from pathlib import Path

def install_cert():
    try:
        import sslserver
        cert_path = Path(sslserver.__file__).parent / 'certs' / 'development.crt'
    except ImportError:
        print("django-sslserver not found. Please ensure it is installed in your environment.")
        return

    if not cert_path.exists():
        print(f"Certificate not found at {cert_path}")
        return

    print(f"Found certificate at: {cert_path}")
    
    cmd = [
        'sudo', 'security', 'add-trusted-cert', 
        '-d', '-r', 'trustRoot', 
        '-k', '/Library/Keychains/System.keychain', 
        str(cert_path)
    ]
    
    print("Running command to trust certificate (requires sudo password):")
    print(" ".join(cmd))
    
    try:
        subprocess.check_call(cmd)
        print("Certificate successfully added to System Keychain. You may need to restart your browser and the application.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to add certificate: {e}")

if __name__ == "__main__":
    install_cert()
