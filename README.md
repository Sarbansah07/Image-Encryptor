🖼 Image Encryption App

A lightweight Flask web application for securely encrypting and decrypting images using either AES (Advanced Encryption Standard) or XOR algorithms.
Runs locally with a simple web interface that lets you upload, process, and download images.

⸻

🚀 Features
	•	🔐 AES-256-CBC encryption for strong security
	•	⚙ XOR encryption for simple demonstrations
	•	🌐 Easy-to-use Flask web interface
	•	💾 Local processing (no cloud uploads)
	•	🧠 Learn-by-doing example of cryptographic file handling

⸻

📂 Project Structure

Image-Encryption-App/
│
├── app.py                # Flask backend (AES & XOR logic)
├── templates/
│   └── index.html        # Frontend upload form
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation


⸻

⚙ Quick Start (Windows PowerShell)

# 1️⃣ Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2️⃣ Install dependencies
pip install -r requirements.txt

# 3️⃣ Set the Flask app and run the server
$env:FLASK_APP = 'd:/ins/app.py'
flask run

Then open your browser and visit:

👉 http://127.0.0.1:5000￼

Upload an image, choose:
	•	Operation: Encrypt or Decrypt
	•	Method: AES or XOR

For AES, provide a password.
For XOR, provide a simple key string.

⸻

🧩 Encryption File Formats

🔹 AES (Recommended)

|--- 'AES' marker (3 bytes)
|--- 16-byte random salt
|--- 16-byte initialization vector (IV)
|--- AES-256-CBC ciphertext

	•	AES key derived from password using PBKDF2-HMAC-SHA256 with 100,000 iterations.
	•	Provides strong, modern encryption suitable for secure applications.

⸻

🔹 XOR (Simple)

|--- 'XOR' marker (3 bytes)
|--- XOR-encrypted image data

	•	Uses a basic bitwise XOR operation with the provided key string.
	•	Not secure, but useful for learning how simple encryption works.

⸻

🔒 Security Overview

Feature	Description
Algorithm	AES-256-CBC with PBKDF2-HMAC-SHA256
Key Derivation	100,000 PBKDF2 iterations for password hardening
Salt & IV	Randomly generated per file
Data Handling	All operations done locally — no uploads
XOR Mode	For educational/demo purposes only


⸻

🧠 Educational Value

This app is great for:
	•	Learning how encryption and decryption work in practice
	•	Understanding file I/O and Flask web app structure
	•	Experimenting with cryptographic algorithms in Python

⸻

🪄 Example Use Case
	1.	Upload any .png or .jpg image.
	2.	Select Encrypt and AES, enter a password.
	3.	Download the encrypted file.
	4.	Later, upload the encrypted file again, choose Decrypt, and use the same password to restore the image.

⸻

⚡ Dependencies

All dependencies are listed in requirements.txt.
Typical libraries include:
	•	Flask – Web framework
	•	cryptography – AES implementation
	•	Werkzeug – File handling utilities

Install with:

pip install -r requirements.txt
