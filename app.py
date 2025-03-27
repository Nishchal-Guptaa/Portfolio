from flask import Flask, render_template, request, redirect, url_for
import requests
from pymongo import MongoClient

app = Flask(__name__)

MONGO_URI = "mongodb://localhost:27017/"  # Replace with your MongoDB Atlas URI if needed
client = MongoClient(MONGO_URI)
db = client["contact_db"]  # Create a database
contacts = db["contacts"]  # Create a collection

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projects')
def projects():
    github_username = 'Nishchal-Guptaa'
    url = f'https://api.github.com/users/{github_username}/repos'
    headers = {
        'AUTHORIZATION':'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'
    }
    response = requests.get(url, headers=headers)
    projects = response.json()
    return render_template('projects.html', projects=projects)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route("/submit", methods=["POST"])
def submit_form():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # Insert data into MongoDB
        contact_data = {"name": name, "email": email, "message": message}
        contacts.insert_one(contact_data)

        return redirect(url_for("contact"))  # Redirect after submission

if __name__ == '__main__':
    app.run(debug=True)