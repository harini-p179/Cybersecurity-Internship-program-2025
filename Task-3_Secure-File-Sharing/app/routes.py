import io
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, session, jsonify
from werkzeug.utils import secure_filename
from app.crypto import FileEncryption
from app.utils import allowed_file, get_file_info
import os
import uuid
from datetime import datetime
from config import Config

main = Blueprint('main', __name__)
crypto = FileEncryption()

@main.route('/')
def index():
    """Main page with file upload and download options"""
    return render_template('index.html')

@main.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """Handle file upload with encryption"""
    if request.method == 'POST':
        try:
            # Check if file was uploaded
            if 'file' not in request.files:
                flash('No file selected', 'error')
                return redirect(request.url)
            
            file = request.files['file']
            
            # Check if file was selected
            if file.filename == '':
                flash('No file selected', 'error')
                return redirect(request.url)
            
            # Check if file type is allowed
            if not allowed_file(file.filename):
                flash('File type not allowed', 'error')
                return redirect(request.url)
            
            # Read file data
            file_data = file.read()
            print(f"File read successfully: {len(file_data)} bytes")
            
            # Encrypt the file
            encrypted_data, key, iv = crypto.encrypt_file(file_data)
            print(f"File encrypted successfully: {len(encrypted_data)} bytes")
            
            # Generate unique filename
            original_filename = secure_filename(file.filename)
            file_extension = os.path.splitext(original_filename)[1]
            unique_filename = f"{uuid.uuid4().hex}{file_extension}"
            print(f"Generated filename: {unique_filename}")
            
            # Ensure directories exist
            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
            os.makedirs(Config.KEY_FOLDER, exist_ok=True)
            print(f"Directories created/verified: {Config.UPLOAD_FOLDER}, {Config.KEY_FOLDER}")
            
            # Save encrypted file
            encrypted_file_path = os.path.join(Config.UPLOAD_FOLDER, unique_filename)
            with open(encrypted_file_path, 'wb') as f:
                f.write(encrypted_data)
            print(f"Encrypted file saved: {encrypted_file_path}")
            
            # Save key information
            key_file_path = crypto.save_key_info(unique_filename, key, iv)
            print(f"Key file saved: {key_file_path}")
            
            # Store file information in session for download
            if 'files' not in session:
                session['files'] = {}
            
            session['files'][unique_filename] = {
                'original_name': original_filename,
                'upload_time': datetime.now().isoformat(),
                'size': len(file_data),
                'hash': crypto.calculate_file_hash(file_data),
                'encrypted_size': len(encrypted_data)
            }
            
            # Force session to be saved
            session.modified = True
            print(f"Session updated with file info")
            
            flash(f'File "{original_filename}" uploaded and encrypted successfully!', 'success')
            print(f"Upload completed successfully")
            return redirect(url_for('main.download_files'))
            
        except Exception as e:
            print(f"Error during upload: {str(e)}")
            flash(f'Error during upload: {str(e)}', 'error')
            return redirect(request.url)
    
    return render_template('upload.html')

@main.route('/download')
def download_files():
    """Show list of uploaded files"""
    files = session.get('files', {})
    print(f"Files in session: {list(files.keys())}")
    return render_template('download.html', files=files)

@main.route('/download/<filename>')
def download_file(filename):
    """Download and decrypt a file"""
    files = session.get('files', {})
    
    if filename not in files:
        flash('File not found', 'error')
        return redirect(url_for('main.download_files'))
    
    # Load key information
    key, iv = crypto.load_key_info(filename)
    
    if key is None or iv is None:
        flash('Encryption key not found', 'error')
        return redirect(url_for('main.download_files'))
    
    # Read encrypted file
    encrypted_file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    
    if not os.path.exists(encrypted_file_path):
        flash('Encrypted file not found', 'error')
        return redirect(url_for('main.download_files'))
    
    with open(encrypted_file_path, 'rb') as f:
        encrypted_data = f.read()
    
    # Decrypt the file
    try:
        decrypted_data = crypto.decrypt_file(encrypted_data, key, iv)
        
        # Verify file integrity
        calculated_hash = crypto.calculate_file_hash(decrypted_data)
        stored_hash = files[filename]['hash']
        
        if calculated_hash != stored_hash:
            flash('File integrity check failed!', 'error')
            return redirect(url_for('main.download_files'))
        
        # Return decrypted file
        original_filename = files[filename]['original_name']
        return send_file(
            io.BytesIO(decrypted_data),
            as_attachment=True,
            download_name=original_filename,
            mimetype='application/octet-stream'
        )
        
    except Exception as e:
        flash(f'Error decrypting file: {str(e)}', 'error')
        return redirect(url_for('main.download_files'))

@main.route('/decrypt-info/<filename>')
def decrypt_info(filename):
    """Show decryption information for a file"""
    files = session.get('files', {})
    
    if filename not in files:
        return jsonify({'error': 'File not found'}), 404
    
    # Load key information
    key, iv = crypto.load_key_info(filename)
    
    if key is None or iv is None:
        return jsonify({'error': 'Encryption key not found'}), 404
    
    file_info = files[filename]
    
    return jsonify({
        'filename': file_info['original_name'],
        'upload_time': file_info['upload_time'],
        'original_size': file_info['size'],
        'encrypted_size': file_info.get('encrypted_size', 'Unknown'),
        'hash': file_info['hash'],
        'key_length': len(key) * 8,  # Key size in bits
        'iv_length': len(iv) * 8,    # IV size in bits
        'encryption_algorithm': 'AES-256-CBC',
        'hash_algorithm': 'SHA-256'
    })

@main.route('/verify-integrity/<filename>')
def verify_integrity(filename):
    """Verify file integrity without downloading"""
    files = session.get('files', {})
    
    if filename not in files:
        return jsonify({'error': 'File not found'}), 404
    
    # Load key information
    key, iv = crypto.load_key_info(filename)
    
    if key is None or iv is None:
        return jsonify({'error': 'Encryption key not found'}), 404
    
    # Read encrypted file
    encrypted_file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    
    if not os.path.exists(encrypted_file_path):
        return jsonify({'error': 'Encrypted file not found'}), 404
    
    with open(encrypted_file_path, 'rb') as f:
        encrypted_data = f.read()
    
    try:
        # Decrypt the file
        decrypted_data = crypto.decrypt_file(encrypted_data, key, iv)
        
        # Calculate hash
        calculated_hash = crypto.calculate_file_hash(decrypted_data)
        stored_hash = files[filename]['hash']
        
        integrity_valid = calculated_hash == stored_hash
        
        return jsonify({
            'filename': files[filename]['original_name'],
            'integrity_valid': integrity_valid,
            'calculated_hash': calculated_hash,
            'stored_hash': stored_hash,
            'file_size': len(decrypted_data),
            'encrypted_size': len(encrypted_data)
        })
        
    except Exception as e:
        return jsonify({'error': f'Decryption failed: {str(e)}'}), 500

@main.route('/delete/<filename>')
def delete_file(filename):
    """Delete a file and its encryption key"""
    files = session.get('files', {})
    
    if filename not in files:
        flash('File not found', 'error')
        return redirect(url_for('main.download_files'))
    
    # Delete encrypted file
    encrypted_file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    if os.path.exists(encrypted_file_path):
        os.remove(encrypted_file_path)
    
    # Delete key file
    key_file_path = os.path.join(Config.KEY_FOLDER, f"{filename}.key")
    if os.path.exists(key_file_path):
        os.remove(key_file_path)
    
    # Remove from session
    del session['files'][filename]
    session.modified = True
    
    flash('File deleted successfully', 'success')
    return redirect(url_for('main.download_files'))

# Add a debug route to check system status
@main.route('/debug')
def debug_info():
    """Debug information about the system"""
    debug_info = {
        'upload_folder': Config.UPLOAD_FOLDER,
        'key_folder': Config.KEY_FOLDER,
        'upload_folder_exists': os.path.exists(Config.UPLOAD_FOLDER),
        'key_folder_exists': os.path.exists(Config.KEY_FOLDER),
        'files_in_session': len(session.get('files', {})),
        'session_files': list(session.get('files', {}).keys()),
        'upload_files': os.listdir(Config.UPLOAD_FOLDER) if os.path.exists(Config.UPLOAD_FOLDER) else [],
        'key_files': os.listdir(Config.KEY_FOLDER) if os.path.exists(Config.KEY_FOLDER) else []
    }
    return jsonify(debug_info)
