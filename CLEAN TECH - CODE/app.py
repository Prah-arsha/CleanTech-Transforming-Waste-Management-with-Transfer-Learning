from flask import Flask, render_template, request
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# Initialize Flask app
app = Flask(__name__)

# Load the trained model (make sure this .h5 file is in the same folder as this app.py)
model = load_model('healthy_vs_rotten.h5')

# Define the class labels in the same order as your model was trained
labels = ['Eosinophil', 'Lymphocyte', 'Monocyte', 'Neutrophil']

# Route for home page (index.html)
@app.route('/')
def home():
    return render_template('index.html')

# Route for project info page (portfolio-details.html)
@app.route('/portfolio')
def portfolio():
    return render_template('portfolio-details.html')

# Route for prediction result (after uploading image)
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return 'No image uploaded!', 400

    # Save uploaded file to static/uploads/
    file = request.files['image']
    upload_path = os.path.join('static/uploads', file.filename)
    file.save(upload_path)

    # Preprocess the image to match the model input
    img = image.load_img(upload_path, target_size=(224, 224))  # Change size based on your model
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    # Predict the class
    predictions = model.predict(img_array)
    predicted_class = labels[np.argmax(predictions)]

    # Return the result.html page with prediction
    return render_template('result.html', prediction=predicted_class)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
