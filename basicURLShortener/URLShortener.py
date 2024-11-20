from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

# Dictionary to store URL mappings
url_mapping = {}
base_url = "http://localhost:5000/"

# Generate a short URL key
def generate_short_key(url):
    return str(hash(url))[:6]  # Use the first 6 characters of the hash as the key

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """
    API endpoint to shorten a URL.
    Expects JSON input: {"long_url": "http://example.com"}
    """
    data = request.json
    if not data or 'long_url' not in data:
        return jsonify({"error": "Invalid request, 'long_url' is required"}), 400

    long_url = data['long_url']
    short_key = generate_short_key(long_url)

    if short_key not in url_mapping:
        url_mapping[short_key] = long_url

    short_url = base_url + short_key
    return jsonify({"short_url": short_url, "long_url": long_url})

@app.route('/<short_key>', methods=['GET'])
def redirect_to_long_url(short_key):
    """
    Redirects a short URL to the original long URL.
    """
    long_url = url_mapping.get(short_key)
    if not long_url:
        return jsonify({"error": "Short URL not found"}), 404

    return redirect(long_url, code=302)

@app.route('/all', methods=['GET'])
def get_all_mappings():
    """
    Returns all URL mappings for debugging.
    """
    return jsonify(url_mapping)

if __name__ == '__main__':
    app.run(debug=True)
