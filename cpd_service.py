from flask import Flask, request, jsonify, send_file, render_template
import numpy as np  # If needed for data manipulation
import pandas as pd
import os
import CPD_helper as helper
# Import your autoencoder model and any preprocessing functions

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/cpd_home')
def upload_page():
    return render_template('cpd_home.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file'] 

    # If user does not select file, browser also submit an empty part without filename
    if file.filename == '':
        return 'No selected file'
 
    if file and allowed_file(file.filename):
        # Save the uploaded file to the UPLOAD_FOLDER
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Process the uploaded Excel file (e.g., read data)
        helper.preprocess_data(file_path)

    else:
        return 'Invalid file type'

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from the request
        input_data = request.json['data']  # Assuming JSON data is sent in the request

        # Preprocess the input data if needed
        # ...

        # Pass the input data through the autoencoder model
        # reconstructed_data = your_autoencoder_model.predict(input_data)

        # Return the reconstructed output as JSON response
        return jsonify({'reconstructed_data': input_data.tolist()})  # Convert to list if needed

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode
