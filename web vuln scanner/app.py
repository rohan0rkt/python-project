from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__, template_folder=os.getcwd())  # Set current directory as template folder

def check_security_headers(url):
    try:
        response = requests.get(url)
        headers = response.headers
        security_headers = ["Content-Security-Policy", "X-Frame-Options", "X-XSS-Protection", "Strict-Transport-Security"]
        missing_headers = [header for header in security_headers if header not in headers]
        return {"missing_headers": missing_headers}
    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def home():
    return render_template("index.html")  # Load the frontend

@app.route("/scan", methods=["POST"])
def scan():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    security_results = check_security_headers(url)
    return jsonify(security_results)

if __name__ == "__main__":
    app.run(debug=True)
