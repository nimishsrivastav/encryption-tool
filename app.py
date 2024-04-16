from flask import Flask, render_template, request, redirect, send_file, url_for

import os

# Importing encryption and decryption functions
from tool.encrypt_file import encrypt_file
from tool.decrypt_file import decrypt_file

app = Flask(__name__)

# Folder structure and allowed file extensions
BASE_FOLDER = 'files'
UPLOAD_FOLDER = os.path.join(BASE_FOLDER, 'uploaded_files')
ENCRYPTED_FOLDER = os.path.join(BASE_FOLDER, 'encrypted_files')
DECRYPTED_FOLDER = os.path.join(BASE_FOLDER, 'decrypted_files')
ALLOWED_EXTENSIONS = {'txt', 'doc', 'docx', 'xls', 'xlsx', 'json', 'xml'}               # The tool will work with files having the extensions mentioned here

# Create folder structure if doesn't exist
for folder in [BASE_FOLDER, UPLOAD_FOLDER, ENCRYPTED_FOLDER, DECRYPTED_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER                 # Uploaded files will be saved in this folder
app.config['ENCRYPTED_FOLDER'] = ENCRYPTED_FOLDER           # Encrypted files will be saved in this folder
app.config['DECRYPTED_FOLDER'] = DECRYPTED_FOLDER           # Decrypted files will be saved in this folder

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():   
    file = request.files['file']

    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        # Check if Encryption button was clicked
        if 'encrypt' in request.form:
            return redirect('/encrypt/' + file.filename)
        # Check if Decryption button was clicked
        elif 'decrypt' in request.form:
            return redirect('/decrypt/' + file.filename)
    else:
        error_message = 'File extension not allowed. Allowed extensions are: ' + ', '.join(ALLOWED_EXTENSIONS)
        return render_template('index.html', error=error_message)

    # Stay on same page after file is uploaded
    return '', 204

@app.route('/encrypt/<filename>', methods=['GET', 'POST'])
def encrypt(filename):
    if request.method == 'POST':
        password = request.form['password']
        
        hash_algorithm = request.form['hash_algorithm']
        algorithm = request.form['algorithm']

        encrypt_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['ENCRYPTED_FOLDER'], filename), password, hash_algorithm, algorithm)
        
        return redirect('/download/' + filename)
    
    return render_template('encrypt.html', filename=filename)

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(app.config['ENCRYPTED_FOLDER'], filename), as_attachment=True)

@app.route('/decrypt/<filename>', methods=['GET', 'POST'])
def decrypt(filename):
    if request.method == 'POST':
        password = request.form['password']

        hash_algorithm = request.form['hash_algorithm']

        decrypt_file(os.path.join(app.config['ENCRYPTED_FOLDER'], filename), os.path.join(app.config['DECRYPTED_FOLDER'], filename), password, hash_algorithm)
        
        return redirect('/download_decrypted/' + filename)
    
    return render_template('decrypt.html', filename=filename)

@app.route('/download_decrypted/<filename>')
def download_decrypted(filename):
    return send_file(os.path.join(app.config['DECRYPTED_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
