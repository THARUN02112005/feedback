from flask import Flask, render_template, request
from datetime import datetime
import csv
from werkzeug.utils import secure_filename
import os
import secrets
import string
def generate_token(length=8):
    characters = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(characters) for _ in range(length))
    return token


app = Flask(__name__)

def collect_feedback(name, email, feedback, image_filename):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("feedback.csv", "a", newline="") as csvfile:
        fieldnames = ["Timestamp", "Name", "Email", "Feedback", "Image"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if csvfile.tell() == 0:
            writer.writeheader()
        
        writer.writerow({
            "Timestamp": timestamp,
            "Name": name,
            "Email": email,
            "Feedback": feedback,
            "Image": image_filename
        })

@app.route("/", methods=["GET", "POST"])
def index():
    feedback_count = 0  # Initialize feedback count

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        feedback = request.form["feedback"]
        image = request.files["image"]
        
        if image.filename:
            image.save(image.filename)
            image_filename = image.filename
        else:
            image_filename = "No Image"
        
        collect_feedback(name, email, feedback, image_filename)
        
        feedback_count += 1  # Update feedback count

        return "Thank you for your feedback! Total feedbacks collected: {}".format(feedback_count)
    
    return render_template("index.html", feedback_count=feedback_count)

@app.route("/feedback_list", methods=["GET"])
def feedback_list():
    feedback_data = []

    with open("feedback.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            feedback_data.append(row)

    return render_template("feedback_list.html", feedback_data=feedback_data)

if __name__ == "__main__":
    app.run(debug=True)
