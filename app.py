"""
Flask Web Application for PDF to Audio Converter
Provides a modern web interface for converting PDFs to audio
"""

from flask import Flask, request, jsonify, send_file, render_template, send_from_directory
from werkzeug.utils import secure_filename
from pdf_to_audio import PDFToAudioConverter
from providers import get_available_providers
import os
import uuid
import time
import threading
import zipfile
from io import BytesIO
from datetime import datetime, timedelta

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Store conversion jobs in memory
# Format: {job_id: {status, progress, message, files, created_at}}
conversion_jobs = {}

# Lock for thread-safe access to conversion_jobs
jobs_lock = threading.Lock()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def cleanup_old_files():
    """Remove files older than 1 hour"""
    current_time = datetime.now()
    cutoff_time = current_time - timedelta(hours=1)

    # Clean up uploads
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename == '.gitkeep':
            continue
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(filepath):
            file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            if file_time < cutoff_time:
                try:
                    os.remove(filepath)
                except Exception as e:
                    print(f"Error removing {filepath}: {e}")

    # Clean up outputs
    for filename in os.listdir(OUTPUT_FOLDER):
        if filename == '.gitkeep':
            continue
        filepath = os.path.join(OUTPUT_FOLDER, filename)
        if os.path.isfile(filepath):
            file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            if file_time < cutoff_time:
                try:
                    os.remove(filepath)
                except Exception as e:
                    print(f"Error removing {filepath}: {e}")

    # Clean up old jobs from memory
    with jobs_lock:
        jobs_to_remove = []
        for job_id, job_data in conversion_jobs.items():
            if job_data.get('created_at', current_time) < cutoff_time:
                jobs_to_remove.append(job_id)
        for job_id in jobs_to_remove:
            del conversion_jobs[job_id]


def run_conversion(job_id, pdf_path, api_key, api_url, provider_name, voice_settings, output_dir):
    """Run PDF to audio conversion in background thread"""
    try:
        with jobs_lock:
            conversion_jobs[job_id]['status'] = 'processing'
            conversion_jobs[job_id]['message'] = 'Initializing converter...'

        # Create converter with custom API URL if provided
        provider_config = {"timeout": 120}
        if api_url:
            provider_config["api_url"] = api_url

        converter = PDFToAudioConverter(
            provider_name=provider_name,
            api_key=api_key,
            provider_config=provider_config
        )

        with jobs_lock:
            conversion_jobs[job_id]['message'] = 'Extracting text from PDF...'

        # Extract text
        text = converter.extract_text_from_pdf(pdf_path)

        if not text or not text.strip():
            with jobs_lock:
                conversion_jobs[job_id]['status'] = 'error'
                conversion_jobs[job_id]['message'] = 'Could not extract text from PDF. The PDF may be image-based or empty.'
            return

        # Split text into chunks
        chunks = converter.split_text(text)
        total_chunks = len(chunks)

        with jobs_lock:
            conversion_jobs[job_id]['message'] = f'Converting {total_chunks} text chunk(s) to audio...'
            conversion_jobs[job_id]['total_chunks'] = total_chunks

        # Convert each chunk
        generated_files = []
        pdf_basename = os.path.splitext(os.path.basename(pdf_path))[0]

        for i, chunk in enumerate(chunks, 1):
            with jobs_lock:
                conversion_jobs[job_id]['progress'] = int((i - 1) / total_chunks * 100)
                conversion_jobs[job_id]['message'] = f'Converting part {i} of {total_chunks}...'

            # Generate output filename
            if total_chunks == 1:
                output_filename = f"{pdf_basename}.mp3"
            else:
                output_filename = f"{pdf_basename}_part{i}.mp3"

            output_path = os.path.join(output_dir, output_filename)

            # Convert chunk to audio
            success = converter.provider.text_to_speech(
                text=chunk,
                output_path=output_path,
                voice_settings=voice_settings
            )

            if success:
                file_size = os.path.getsize(output_path)
                generated_files.append({
                    'filename': output_filename,
                    'size': file_size,
                    'size_mb': round(file_size / (1024 * 1024), 2)
                })
            else:
                with jobs_lock:
                    conversion_jobs[job_id]['status'] = 'error'
                    conversion_jobs[job_id]['message'] = f'Failed to convert part {i}'
                return

        # Conversion complete
        with jobs_lock:
            conversion_jobs[job_id]['status'] = 'completed'
            conversion_jobs[job_id]['progress'] = 100
            conversion_jobs[job_id]['message'] = 'Conversion completed successfully!'
            conversion_jobs[job_id]['files'] = generated_files

    except Exception as e:
        with jobs_lock:
            conversion_jobs[job_id]['status'] = 'error'
            conversion_jobs[job_id]['message'] = f'Conversion failed: {str(e)}'


@app.route('/')
def index():
    """Serve main interface"""
    cleanup_old_files()  # Clean up old files on each page load
    return render_template('index.html')


@app.route('/api/providers', methods=['GET'])
def get_providers():
    """Get available TTS providers"""
    try:
        providers = get_available_providers()
        return jsonify({'success': True, 'providers': providers})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/voices/<provider>', methods=['GET'])
def get_voices(provider):
    """Get available voices for a provider"""
    try:
        # Create a temporary converter to get voice info
        # We don't need a valid API key just to get available voices
        converter = PDFToAudioConverter(
            provider_name=provider,
            api_key='dummy_key_for_voice_list',
            provider_config={}
        )
        voices = converter.provider.get_available_voices()
        default_settings = converter.provider.get_default_voice_settings()

        return jsonify({
            'success': True,
            'voices': voices,
            'default_settings': default_settings
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/convert', methods=['POST'])
def convert():
    """Handle PDF upload and conversion"""
    try:
        # Validate request
        if 'pdf_file' not in request.files:
            return jsonify({'success': False, 'error': 'No PDF file provided'}), 400

        file = request.files['pdf_file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Only PDF files are allowed'}), 400

        # Get parameters
        api_key = request.form.get('api_key', '').strip()
        if not api_key:
            return jsonify({'success': False, 'error': 'API key is required'}), 400

        api_url = request.form.get('api_url', '').strip()
        provider_name = request.form.get('provider', 'minimax')

        # Get voice settings
        voice_settings = {}
        if request.form.get('voice_id'):
            voice_settings['voice_id'] = request.form.get('voice_id')
        if request.form.get('speed'):
            voice_settings['speed'] = float(request.form.get('speed'))
        if request.form.get('pitch'):
            voice_settings['pitch'] = int(request.form.get('pitch'))
        if request.form.get('emotion'):
            voice_settings['emotion'] = request.form.get('emotion')
        if request.form.get('vol'):
            voice_settings['vol'] = float(request.form.get('vol'))

        # Generate unique job ID
        job_id = str(uuid.uuid4())

        # Save uploaded file
        filename = secure_filename(file.filename)
        unique_filename = f"{job_id}_{filename}"
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(pdf_path)

        # Create output directory for this job
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], job_id)
        os.makedirs(output_dir, exist_ok=True)

        # Initialize job status
        with jobs_lock:
            conversion_jobs[job_id] = {
                'status': 'queued',
                'progress': 0,
                'message': 'Job queued...',
                'files': [],
                'created_at': datetime.now()
            }

        # Start conversion in background thread
        thread = threading.Thread(
            target=run_conversion,
            args=(job_id, pdf_path, api_key, api_url, provider_name, voice_settings, output_dir)
        )
        thread.daemon = True
        thread.start()

        return jsonify({
            'success': True,
            'job_id': job_id,
            'message': 'Conversion started'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/progress/<job_id>', methods=['GET'])
def get_progress(job_id):
    """Get conversion progress"""
    with jobs_lock:
        if job_id not in conversion_jobs:
            return jsonify({'success': False, 'error': 'Job not found'}), 404

        job_data = conversion_jobs[job_id].copy()

    return jsonify({
        'success': True,
        'job_id': job_id,
        'status': job_data.get('status', 'unknown'),
        'progress': job_data.get('progress', 0),
        'message': job_data.get('message', ''),
        'files': job_data.get('files', [])
    })


@app.route('/api/download/<job_id>/<filename>', methods=['GET'])
def download_file(job_id, filename):
    """Download a specific audio file"""
    try:
        # Security: ensure filename doesn't contain path traversal
        safe_filename = secure_filename(filename)
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], job_id, safe_filename)

        if not os.path.exists(file_path):
            return jsonify({'success': False, 'error': 'File not found'}), 404

        return send_file(file_path, as_attachment=True, download_name=safe_filename)

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/download-all/<job_id>', methods=['GET'])
def download_all(job_id):
    """Download all audio files as a ZIP"""
    try:
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], job_id)

        if not os.path.exists(output_dir):
            return jsonify({'success': False, 'error': 'Job not found'}), 404

        # Create ZIP file in memory
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for filename in os.listdir(output_dir):
                file_path = os.path.join(output_dir, filename)
                if os.path.isfile(file_path):
                    zf.write(file_path, filename)

        memory_file.seek(0)

        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'audio_files_{job_id}.zip'
        )

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))

    # Run Flask app
    print(f"\n{'='*60}")
    print(f"🎙️  PDF to Audio Converter")
    print(f"{'='*60}")
    print(f"🌐 Server running on: http://localhost:{port}")
    print(f"📱 Or access from other devices: http://0.0.0.0:{port}")
    print(f"{'='*60}\n")

    app.run(debug=True, host='0.0.0.0', port=port)
