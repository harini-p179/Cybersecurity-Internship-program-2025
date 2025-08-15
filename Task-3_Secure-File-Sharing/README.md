# 🔐 Secure File Sharing System

A military-grade secure file sharing system built with Python Flask and AES-256 encryption.

## �� Features

- **AES-256-CBC Encryption**: Industry-standard encryption for all files
- **Unique Key Management**: Each file gets its own encryption key and IV
- **File Integrity Verification**: SHA-256 hash verification on download
- **Session-based Access**: Secure file access through Flask sessions
- **Modern UI**: Beautiful, responsive web interface
- **File Type Validation**: Restricted file types for security

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Encryption**: PyCryptodome (AES-256-CBC)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with modern design
- **Icons**: Font Awesome

## 📋 Prerequisites

- Python 3.7+
- pip (Python package installer)

## 🚀 Installation & Setup

1. **Navigate to the project directory**
   ```bash
   cd Users/honey/Cybersecurity-Internship-Program-2025/Task-3_Secure-File-Sharing
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 🔐 Security Features

### Encryption
- **Algorithm**: AES-256-CBC
- **Key Generation**: Cryptographically secure random keys
- **IV Generation**: Unique initialization vectors for each file
- **Padding**: PKCS7 padding for variable-length data

### Key Management
- **Unique Keys**: Each file gets its own encryption key
- **Secure Storage**: Keys stored separately from encrypted files
- **Base64 Encoding**: Keys stored in human-readable format

### File Integrity
- **SHA-256 Hashing**: Cryptographic hash verification
- **Hash Storage**: File hashes stored in session data
- **Download Verification**: Hash verification on file download

## 📁 Project Structure

```
Task-3_Secure-File-Sharing/
├── app/                    # Application package
│   ├── __init__.py        # Flask app factory
│   ├── routes.py          # Route definitions
│   ├── crypto.py          # Encryption/decryption logic
│   └── utils.py           # Utility functions
├── static/                # Static files
│   ├── css/
│   │   └── style.css      # Custom styles
│   └── js/
│       └── main.js        # JavaScript functionality
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Home page
│   ├── upload.html        # Upload page
│   └── download.html      # Download page
├── uploads/               # Encrypted file storage
├── keys/                  # Encryption key storage
├── requirements.txt       # Python dependencies
├── config.py             # Configuration settings
├── run.py                # Application entry point
└── README.md             # This file
```

## 🔄 Usage

### Uploading Files
1. Navigate to the upload page
2. Select a file (max 16MB, allowed types only)
3. Click "Encrypt & Upload"
4. File is encrypted and stored securely

### Downloading Files
1. Go to the download page
2. View list of uploaded files
3. Click "Download" to retrieve and decrypt
4. File integrity is automatically verified

### Deleting Files
1. On the download page, click "Delete" next to any file
2. Confirm deletion
3. Both encrypted file and key are permanently removed

## 🧪 Testing

To test the system:

1. Start the application
2. Upload a test file
3. Verify it appears in the download list
4. Download the file and verify it matches the original
5. Check that the downloaded file opens correctly

## 🔒 Security Considerations

- **Key Storage**: Keys are stored in plain text files (for demo purposes)
- **Session Security**: Uses Flask sessions for file access
- **File Validation**: Only allows specific file types
- **Size Limits**: Enforces maximum file size limits
- **Integrity Checks**: SHA-256 hash verification on download

## 📝 License

This project is part of the Cybersecurity Internship Program 2025.

## 🧠 Contributing

This is an educational project for cybersecurity internship training.

```

## 12. Create a security documentation file:

```markdown:Users/honey/Cybersecurity-Internship-Program-2025/Task-3_Secure-File-Sharing/SECURITY.md
# 🔒 Se
