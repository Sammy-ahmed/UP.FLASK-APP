from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Define the folder to store files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home route that shows a list of uploaded files
@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

# Route to upload a file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename != '':
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return redirect(url_for('index'))

# Route to delete a file
@app.route('/delete/<filename>')
def delete_file(filename):
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    except FileNotFoundError:
        pass
    return redirect(url_for('index'))

# Route to update a file's name
@app.route('/update/<filename>', methods=['POST'])
def update_file(filename):
    new_name = request.form['new_name']
    if new_name:
        os.rename (os.path.join(app.config['UPLOAD_FOLDER'], filename),
                os.path.join(app.config['UPLOAD_FOLDER'], new_name))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)