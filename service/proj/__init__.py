import logging
import platform


_DEBUG = False
_STATIC_URL = '/static/'
WINDOWS = 'Windows'
LINUX = 'Linux'
MacOS = 'Darwin'
CURRENT_SYSTEM = platform.system()

if CURRENT_SYSTEM == WINDOWS:
    _DEBUG = True

elif CURRENT_SYSTEM == MacOS:
    _DEBUG = True
else:
    """
        服务器环境 
    """
logging.info(f"this app is running on {CURRENT_SYSTEM},DEBUG:{_DEBUG}")
