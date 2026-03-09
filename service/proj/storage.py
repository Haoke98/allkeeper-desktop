import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from cryptography.fernet import Fernet
import base64
from django.core.files.base import ContentFile
from io import BytesIO

class EncryptedFileSystemStorage(FileSystemStorage):
    def __init__(self, location=None, base_url=None, file_permissions_mode=None, directory_permissions_mode=None):
        super().__init__(location, base_url, file_permissions_mode, directory_permissions_mode)
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)

    def _get_or_create_key(self):
        key_path = os.path.join(settings.APP_HOME_DIR, 'secret.key')
        if os.path.exists(key_path):
            with open(key_path, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_path, 'wb') as f:
                f.write(key)
            return key

    def _save(self, name, content):
        # Read content, encrypt it, and save
        content_bytes = content.read()
        encrypted_content = self.cipher.encrypt(content_bytes)
        return super()._save(name, ContentFile(encrypted_content))

    def _open(self, name, mode='rb'):
        f = super()._open(name, mode)
        encrypted_data = f.read()
        try:
            decrypted_data = self.cipher.decrypt(encrypted_data)
            return BytesIO(decrypted_data)
        except Exception:
            # Fallback for unencrypted files (migration path)
            return BytesIO(encrypted_data)
