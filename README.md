# Image Encryption App

This is a small Flask app to encrypt and decrypt images using either AES (recommended) or XOR (simple). It runs locally and returns the processed file for download.

Files added:
- `app.py` - Flask application implementing AES and XOR encrypt/decrypt.
- `templates/index.html` - simple upload form.
- `requirements.txt` - Python dependencies.

Quick start (PowerShell on Windows):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:FLASK_APP = 'd:/ins/app.py'
flask run
```

Open http://127.0.0.1:5000 in your browser. Upload an image and choose Encrypt or Decrypt and the method (AES/XOR). For AES provide a password; for XOR provide a key string.

Notes:
- AES file format: ASCII marker `AES` (3 bytes) + 16-byte salt + 16-byte IV + ciphertext.
- XOR file format: ASCII marker `XOR` (3 bytes) + XORed payload.

Security: AES uses PBKDF2-HMAC-SHA256 with 100k iterations and AES-256-CBC. This is for demo purposes only — treat as educational code and don't use in production without review.
