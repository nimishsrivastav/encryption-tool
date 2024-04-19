from flask import Flask, render_template, request, redirect, send_file, session

import os, time

# Importing encryption and decryption functions
from tool.encrypt_file import encrypt_file
from tool.decrypt_file import decrypt_file

app = Flask(__name__)
app.secret_key = 'secret_key_for_session'                           # Secret key is required for session to display encryption/decryption times on respective pages

# Folder structure and allowed file extensions
BASE_FOLDER         = 'files'
UPLOAD_FOLDER       = os.path.join(BASE_FOLDER, 'uploaded_files')
ENCRYPTED_FOLDER    = os.path.join(BASE_FOLDER, 'encrypted_files')
DECRYPTED_FOLDER    = os.path.join(BASE_FOLDER, 'decrypted_files')
ALLOWED_EXTENSIONS  = {'txt', 'enc', 'doc', 'docx', 'xls', 'xlsx', 'json', 'xml'}               # The tool will work with files having the extensions mentioned here

# Create folder structure if doesn't exist
for folder in [BASE_FOLDER, UPLOAD_FOLDER, ENCRYPTED_FOLDER, DECRYPTED_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['UPLOAD_FOLDER']     = UPLOAD_FOLDER                 # Uploaded files will be saved in this folder
app.config['ENCRYPTED_FOLDER']  = ENCRYPTED_FOLDER              # Encrypted files will be saved in this folder
app.config['DECRYPTED_FOLDER']  = DECRYPTED_FOLDER              # Decrypted files will be saved in this folder

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Homepage route
@app.route('/')
def index():
    return render_template('index.html')

# File is uploaded on homepage, saved in uploaded_files folder
# File operation (encryption/decryption) is selected from this page
@app.route('/', methods=['POST'])
def upload_file():   
    file = request.files['file']

    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))             # If file format is accepted, save it in uploaded_files folder

        if 'encrypt' in request.form:                                                   # If Encryption button is clicked, change the route to /encrypt
            return redirect('/encrypt/' + file.filename)
        elif 'decrypt' in request.form:                                                 # If Decryption button is clicked, change the route to /decrypt
            return redirect('/decrypt/' + file.filename)
    else:
        error_message = 'File extension not allowed. Allowed extensions are: ' + ', '.join(ALLOWED_EXTENSIONS)              # If file format is not accepted, throw an error

        return render_template('index.html', error=error_message)

    # Stay on same page after file is uploaded
    return '', 204

# File encryption route
@app.route('/encrypt/<filename>', methods=['GET', 'POST'])
def encrypt(filename):
    if request.method == 'POST':
        hash_algorithm = request.form['hash_algorithm']                             # Read the hashing algorithm selected on the HTML page
        encryption_algorithm = request.form['algorithm']                            # Read the encryption algorithm selected on the HTML page
        iterations = int(request.form['iterations'])                                # Read the number of iteration entered for password encryption
        password = request.form['password']                                         # Read password from the HTML page

        encrypted_file_extension = ".enc"                                           # File extension for encrypted file
        new_filename = f"{filename}{encrypted_file_extension}"                      # Append the file extension for encrypted file

        encryption_start_time = time.time()                                         # Encryption start time
        encrypt_file(os.path.join(app.config['UPLOAD_FOLDER'], filename),           # Encrypt file function
                     os.path.join(app.config['ENCRYPTED_FOLDER'], new_filename), 
                     password, hash_algorithm, encryption_algorithm, iterations)
        encryption_end_time = time.time()                                           # Encryption end time

        encryption_time = f"{(encryption_end_time - encryption_start_time):.4f}"    # Time taken for file encryption

        # Store encryption_time in session to display encryption time on the page
        session['encryption_time'] = encryption_time
        
        return redirect('/download/' + new_filename)
    
    # Retrieve encryption_time from session
    encryption_time_str = session.pop('encryption_time', None)

    return render_template('encrypt.html', filename=filename, encryption_time=encryption_time_str)

# Download and save the encrypted file to encrypted_files folder
@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(app.config['ENCRYPTED_FOLDER'], filename), as_attachment=True)

# File decryption route
@app.route('/decrypt/<filename>', methods=['GET', 'POST'])
def decrypt(filename):
    if request.method == 'POST':
        password = request.form['password']                                                         # Read password from the HTML page

        new_filename = filename.replace(".enc", "")                                                 # Remove the encrypted file extension

        decryption_start_time = time.time()                                                         # Decryption start time
        error_message, _ = decrypt_file(os.path.join(app.config['ENCRYPTED_FOLDER'], filename),     # Decrypt file function
                     os.path.join(app.config['DECRYPTED_FOLDER'], new_filename), 
                     password)
        decryption_end_time = time.time()                                                           # Decryption end time
        
        if error_message:
            return render_template('decrypt.html', filename=filename, error=error_message)          # Throw error if decryption fails
        
        decryption_time = f"{(decryption_end_time - decryption_start_time):.4f}"                    # Time taken for file decryption

        # Store encryption_time in session to display decryption time on the page
        session['decryption_time'] = decryption_time

        return redirect('/download_decrypted/' + new_filename)
    
    # Retrieve decryption_time from session
    decryption_time_str = session.pop('decryption_time', None)

    return render_template('decrypt.html', filename=filename, decryption_time=decryption_time_str, error=None)

# Download and save the decrypted file to decrypted_files folder
@app.route('/download_decrypted/<filename>')
def download_decrypted(filename):
    return send_file(os.path.join(app.config['DECRYPTED_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
