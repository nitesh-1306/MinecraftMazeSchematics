from flask import Flask, render_template, jsonify

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        image_url = "https://example.com/static/images/sample.jpg"
        zip_url = "https://example.com/static/files/sample.zip"
        
        response = {
            "image_url": image_url,
            "zip_url": zip_url
        }
        return jsonify(response)
    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html'), 500

@app.errorhandler(Exception)
def handle_error(e):
    print(f"Error: {e}")
    return render_template('error.html'), getattr(e, 'code', 500)

if __name__ == '__main__':
    app.run(debug=True)
