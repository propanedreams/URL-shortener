URL Shortener - Flask Application

This is a basic URL Shortener application built with Flask. It allows you to shorten long URLs and access them via short URLs. This is a personal project which will get better with time
Features

    Shorten a URL: Converts a long URL into a short URL.
    Redirect: Access the original URL using the short URL.
    Using sqlite as storage.
    Debugging: View all stored URL mappings.

Prerequisites

    Python 3.x installed on your system.
    Flask installed in your environment. Install Flask using:

    pip install flask

How to Run

    Clone the repository or save the script to your local machine.
    Navigate to the project directory.
    Activate your virtual environment (if applicable).
    Run the Flask app:

    python url_shortener.py

    The app will start on http://localhost:5000.

API Endpoints
1. Shorten a URL

    Endpoint: /shorten
    Method: POST
    Description: Shortens a long URL.
    Request:

{
  "long_url": "https://example.com"
}

Response:

    {
      "short_url": "http://localhost:5000/abc123",
      "long_url": "https://example.com"
    }

Example Command:

curl -X POST -H "Content-Type: application/json" -d '{"long_url": "https://example.com"}' http://localhost:5000/shorten

2. Access Short URL

    Endpoint: /<short_key>
    Method: GET
    Description: Redirects to the original URL using the short key.
    Example: Visiting http://localhost:5000/abc123 will redirect you to https://example.com.

3. View All Mappings

    Endpoint: /all
    Method: GET
    Description: Returns all stored URL mappings for debugging purposes.
    Response:

    {
      "abc123": "https://example.com"
    }

Notes

    The application stores URL mappings in memory. If the app restarts, the mappings will be lost unless persistence is added (e.g., using a database or a file).
    The base URL (http://localhost:5000) can be replaced with a live domain if deployed online.

Troubleshooting

    Flask Not Found: Ensure Flask is installed in your environment:

pip install flask

Short URL Not Found:

    Ensure the short URL exists in the mappings.
    Restarting the app clears the mappings unless persistence is added.
