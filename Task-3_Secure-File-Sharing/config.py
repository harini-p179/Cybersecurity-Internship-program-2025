import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx'}
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Encryption settings
    KEY_SIZE = 32  # 256-bit key for AES-256
    IV_SIZE = 16   # 128-bit IV for AES
    KEY_FOLDER = 'keys'
