from flask import Flask, request, render_template, send_file, flash, redirect, url_for
from io import BytesIO
import os
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from PIL import Image
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

BACKEND = default_backend()

def derive_key(password: bytes, salt: bytes, length: int = 32) -> bytes:
    # PBKDF2-HMAC-SHA256
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=length,
        salt=salt,
        iterations=100_000,
        backend=BACKEND,
    )
    return kdf.derive(password)

def aes_encrypt(data: bytes, password: str) -> bytes:
    salt = os.urandom(16)
    key = derive_key(password.encode('utf-8'), salt)
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded = padder.update(data) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=BACKEND)
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded) + encryptor.finalize()
    # file format: b'AES' + salt(16) + iv(16) + ciphertext
    return b'AES' + salt + iv + ct

def aes_decrypt(blob: bytes, password: str) -> bytes:
    if not blob.startswith(b'AES'):
        raise ValueError('Not an AES file')
    salt = blob[3:19]
    iv = blob[19:35]
    ct = blob[35:]
    key = derive_key(password.encode('utf-8'), salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=BACKEND)
    decryptor = cipher.decryptor()
    padded = decryptor.update(ct) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded) + unpadder.finalize()
    return data

def xor_process(data: bytes, key_str: str) -> bytes:
    if not key_str:
        raise ValueError('XOR key required')
    key = key_str.encode('utf-8')
    out = bytearray(len(data))
    for i, b in enumerate(data):
        out[i] = b ^ key[i % len(key)]
    # prefix to mark XOR
    return b'XOR' + bytes(out)

def xor_reverse(blob: bytes, key_str: str) -> bytes:
    if not blob.startswith(b'XOR'):
        raise ValueError('Not an XOR file')
    key = key_str.encode('utf-8')
    data = blob[3:]
    out = bytearray(len(data))
    for i, b in enumerate(data):
        out[i] = b ^ key[i % len(key)]
    return bytes(out)

def is_image(data: bytes) -> bool:
    try:
        Image.open(BytesIO(data)).verify()
        return True
    except Exception:
        return False


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        method = request.form.get('method')
        action = request.form.get('action')
        key = request.form.get('key', '')

        if not file:
            flash('No file uploaded')
            return redirect(request.url)

        data = file.read()

        # If encrypting, validate that uploaded input is an image
        if action == 'encrypt':
            if not is_image(data):
                flash('Uploaded file is not a valid image')
                return redirect(request.url)

        try:
            if method == 'AES':
                if action == 'encrypt':
                    out = aes_encrypt(data, key)
                    out_name = file.filename + '.aes'
                    mimetype = 'application/octet-stream'
                else:
                    # decrypt
                    out = aes_decrypt(data, key)
                    out_name = (file.filename.replace('.aes', '') or 'decrypted')
                    mimetype = 'image/*'
            else:
                # XOR
                if action == 'encrypt':
                    out = xor_process(data, key)
                    out_name = file.filename + '.xor'
                    mimetype = 'application/octet-stream'
                else:
                    out = xor_reverse(data, key)
                    out_name = (file.filename.replace('.xor', '') or 'decrypted')
                    mimetype = 'image/*'
        except Exception as e:
            flash('Error processing file: ' + str(e))
            return redirect(request.url)

        bio = BytesIO()
        bio.write(out)
        bio.seek(0)
        return send_file(bio, as_attachment=True, download_name=out_name, mimetype=mimetype)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
