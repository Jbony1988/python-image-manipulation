from flask import Flask, render_template, request, send_from_directory
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'image' not in request.files:
            return render_template('index.html', error='No file part')
        
        file = request.files['image']

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return render_template('index.html', error='No selected file')

        # If the file is allowed and valid
        if file and allowed_file(file.filename):
            x = int(request.form['x'])
            y = int(request.form['y'])
            width = int(request.form['width'])
            height = int(request.form['height'])

            # Save the uploaded file
            filename = 'uploaded_image.jpg'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Open the uploaded image file
            image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Convert image to RGB mode if it has an alpha channel
            if image.mode == 'RGBA':
                image = image.convert('RGB')

            # Define the cropping box
            crop_box = (x, y, x + width, y + height)

            # Crop the image using the defined box
            cropped_image = image.crop(crop_box)

            # Save the cropped image
            cropped_filename = 'cropped_' + filename
            cropped_image.save(os.path.join(app.config['UPLOAD_FOLDER'], cropped_filename))

            # Render the template with the cropped image filename
            return render_template('index.html', cropped_image=cropped_filename)

    # If the request method is GET or there was an error, render the template without the cropped image
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
