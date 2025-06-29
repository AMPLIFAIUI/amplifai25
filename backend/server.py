# Main backend server for AMPLIFAI
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/amp', methods=['POST'])
def amp_api():
    # Handle requests to the Amp agent
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run()