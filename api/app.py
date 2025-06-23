from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['GET'])
def add():
    try:
        a = float(request.args.get('a', 0))
        b = float(request.args.get('b', 0))
        result = a + b
        return jsonify({'result': result})
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
