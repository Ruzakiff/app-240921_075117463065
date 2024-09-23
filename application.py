import os
from backgroundremover.bg import remove
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import uuid
import functools
import io
import threading
import time
import base64

app = Flask(__name__)

# Use an environment variable for the API key
API_KEY = os.environ.get('FRONTEND_API_KEY', 'default_frontend_api_key')

# In-memory task status storage
task_status = {}

def require_api_key(view_function):
    @functools.wraps(view_function)
    def decorated_function(*args, **kwargs):
        provided_key = request.headers.get('X-API-Key')
        if provided_key and provided_key == API_KEY:
            return view_function(*args, **kwargs)
        else:
            return jsonify({'error': 'Invalid or missing API key'}), 403
    return decorated_function

def remove_background_from_data(data, task_id):
    try:
        task_status[task_id] = {'status': 'processing'}
        
        img_alpha = remove(data, model_name="u2netp",
                           alpha_matting=True,
                           alpha_matting_foreground_threshold=230,
                           alpha_matting_background_threshold=20,
                           alpha_matting_erode_structure_size=10)
        
        # Convert bytes to base64 string for JSON serialization
        img_base64 = base64.b64encode(img_alpha).decode('utf-8')
        
        task_status[task_id] = {'status': 'completed', 'result': img_base64}
        return img_base64
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        task_status[task_id] = {'status': 'failed', 'error': str(e)}
        return None

def process_image_async(image_data, task_id):
    remove_background_from_data(image_data, task_id)

@app.route('/remove-background', methods=['POST'])
@require_api_key
def api_remove_background():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400
    
    if file:
        image_data = file.read()
        task_id = str(uuid.uuid4())
        
        # Start processing in a separate thread
        thread = threading.Thread(target=process_image_async, args=(image_data, task_id))
        thread.start()
        
        return jsonify({'task_id': task_id}), 202

@app.route('/task-status/<task_id>', methods=['GET'])
@require_api_key
def get_task_status(task_id):
    status = task_status.get(task_id, {'status': 'not_found'})
    if status['status'] == 'completed':
        return jsonify({'status': status['status'], 'result_url': f'/get-result/{task_id}'}), 200
    return jsonify({'status': status['status']}), 200

@app.route('/get-result/<task_id>', methods=['GET'])
@require_api_key
def get_result(task_id):
    result = task_status.get(task_id)
    if result and result['status'] == 'completed':
        img_data = base64.b64decode(result['result'])
        return send_file(
            io.BytesIO(img_data),
            mimetype='image/png',
            as_attachment=True,
            download_name=f'result_{task_id}.png'
        )
    return jsonify({'error': 'Result not found or not ready'}), 404

@app.route('/', methods=['GET', 'POST'])
def default_route():
    return jsonify({
        'status': 'operational'
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)