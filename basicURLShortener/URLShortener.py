from flask import Flask, request, jsonify, redirect
import sqlite3

app = Flask(__name__)
base_url = "http://localhost:5000/"

# Initialize the database
def init_db():
    conn = sqlite3.connect('url_shortener.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_key TEXT UNIQUE NOT NULL,
            long_url TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Generate a short URL key
def generate_short_key(long_url):
    return str(hash(long_url))[:6]

# Save URL mapping to the database
def save_url_mapping(short_key, long_url):
    conn = sqlite3.connect('url_shortener.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO urls (short_key, long_url) VALUES (?, ?)', (short_key, long_url))
        conn.commit()
    except sqlite3.IntegrityError:
        # Handle duplicate short_key errors
        pass
    conn.close()

# Retrieve long URL by short key
def get_long_url(short_key):
    conn = sqlite3.connect('url_shortener.db')
    cursor = conn.cursor()
    cursor.execute('SELECT long_url FROM urls WHERE short_key = ?', (short_key,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """
    Shorten the long URL provided by the user.
    """
    data = request.json
    if not data or 'long_url' not in data:
        return jsonify({"error": "No URL provided!"}), 400

    long_url = data['long_url']
    short_key = generate_short_key(long_url)
    save_url_mapping(short_key, long_url)

    short_url = base_url + short_key
    return jsonify({"short_url": short_url, "long_url": long_url}), 201

@app.route('/<short_key>', methods=['GET'])
def redirect_to_long_url(short_key):
    """
    Redirect to the long URL using the short key.
    """
    long_url = get_long_url(short_key)
    if not long_url:
        return jsonify({"error": "Short URL not found!"}), 404

    return redirect(long_url, code=302)

@app.route('/all', methods=['GET'])
def get_all_urls():
    """
    Retrieve all URL mappings for debugging purposes.
    """
    conn = sqlite3.connect('url_shortener.db')
    cursor = conn.cursor()
    cursor.execute('SELECT short_key, long_url FROM urls')
    results = cursor.fetchall()
    conn.close()

    url_mappings = [{"short_key": row[0], "long_url": row[1]} for row in results]
    return jsonify(url_mappings), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
