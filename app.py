from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv
import os
import uuid
from datetime import datetime, timedelta
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(override=True)

# Verificar que las variables de entorno estén cargadas
admin_username = os.getenv('ADMIN_USERNAME')
admin_password = os.getenv('ADMIN_PASSWORD')
secret_key = os.getenv('SECRET_KEY')

# Debug print para verificar valores cargados
print("Variables de entorno cargadas:")
print(f"ADMIN_USERNAME: '{admin_username}'")
print(f"ADMIN_PASSWORD: '{admin_password}'")
print(f"SECRET_KEY length: {len(secret_key) if secret_key else 0}")

if not all([admin_username, admin_password, secret_key]):
    raise ValueError("Error: No se pudieron cargar las variables de entorno")

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Session duration
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'txt', 'zip', 'rar', 'mp3', 'mp4', 'xls', 'xlsx', 'ppt', 'pptx', 'csv'}

# Ensure directories exist
for directory in [app.config['UPLOAD_FOLDER'], 'static/images']:
    try:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Directory created/verified: {directory}")
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {str(e)}")
        raise

# Login manager configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página'
login_manager.login_message_category = 'error'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if user_id == admin_username:
        return User(user_id)
    return None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_unique_filename(original_filename):
    try:
        # Mantener el nombre original pero añadir un UUID al principio
        name, ext = os.path.splitext(original_filename)
        return f"{unique_id}-{secure_filename(name)}{ext}"
    except Exception as e:
        logger.error(f"Error generating unique filename: {str(e)}")
        return secure_filename(original_filename)

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Debug print para verificar valores
        print(f"Login attempt - Username provided: '{username}', Expected: '{admin_username}'")
        print(f"Password provided: '{password}', Expected: '{admin_password}'")
        
        if username == admin_username and password == admin_password:
            user = User(username)
            login_user(user, remember=True)
            session.permanent = True
            flash('¡Welcome!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        flash('You have successfully logged out', 'success')
        logger.info("User logged out successfully")
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        flash('Error al cerrar sesión', 'error')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        files = []
        upload_dir = os.path.abspath(app.config['UPLOAD_FOLDER'])
        
        # Asegurarse de que el directorio existe
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            
        for filename in os.listdir(upload_dir):
            if allowed_file(filename):
                file_path = os.path.join(upload_dir, filename)
                try:
                    file_stats = os.stat(file_path)
                    files.append({
                        'name': filename,
                        'size': file_stats.st_size,
                        'date': datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                        'url': url_for('uploaded_file', filename=filename)
                    })
                except OSError as e:
                    logger.error(f"Error getting file stats for {filename}: {str(e)}")
                    continue
                    
        # Ordenar archivos por fecha de modificación, más recientes primero
        files.sort(key=lambda x: x['date'], reverse=True)
        
        # Debug log
        logger.info(f"Found {len(files)} files in upload directory")
        for file in files:
            logger.info(f"File: {file['name']}, URL: {file['url']}")
            
        return render_template('dashboard.html', files=files)
    except Exception as e:
        logger.error(f"Error in dashboard: {str(e)}")
        flash('Error al cargar los archivos', 'error')
        return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400
    
    if not file or not allowed_file(file.filename):
        return jsonify({'error': 'Tipo de archivo no permitido'}), 400
    
    try:
        # Generate unique filename
        filename = generate_unique_filename(file.filename)
        
        # Guardar archivo
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        logger.info(f"File saved successfully: {filename}")
            
        return jsonify({
            'message': 'File uploaded successfully',
            'filename': filename,
            'url': url_for('uploaded_file', filename=filename)
        })
    except Exception as e:
        logger.error(f"Error during file upload: {str(e)}")
        return jsonify({'error': 'Error al subir el archivo'}), 500

@app.route('/delete/<filename>', methods=['DELETE'])
@login_required
def delete_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"File deleted: {filename}")
            
        return jsonify({'message': 'File deleted successfully'})
    except Exception as e:
        logger.error(f"Error deleting file {filename}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    try:
        # Asegurarse de que el archivo existe
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            logger.error(f"File not found: {filename}")
            return 'File not found', 404
            
        # Verificar que el archivo está en el directorio permitido
        if not os.path.abspath(file_path).startswith(os.path.abspath(app.config['UPLOAD_FOLDER'])):
            logger.error(f"Invalid file path: {filename}")
            return 'Invalid file path', 403
            
        return send_from_directory(
            os.path.abspath(app.config['UPLOAD_FOLDER']), 
            filename,
            as_attachment=False,
            mimetype=None
        )
    except Exception as e:
        logger.error(f"Error serving file {filename}: {str(e)}")
        return str(e), 500

@app.route('/share/<filename>')
def share_file(filename):
    if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        flash('File does not exist', 'error')
        return redirect(url_for('dashboard'))
    return render_template('share.html', filename=filename)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error='Internal server error'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
