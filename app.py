from datetime import date
from flask import Flask, render_template, request

app = Flask(__name__)

@app.context_processor
def inject_helpers():
    def is_active(endpoint):
        return "active fw-bold text-decoration-underline" if request.endpoint == endpoint else ""
    
    return {
        "is_active": is_active,
        "site_name": "MiniBlog",
        "current_year": date.today().year,
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(port=8000, debug=True)