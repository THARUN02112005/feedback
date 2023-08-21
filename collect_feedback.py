from flask import Flask, render_template, request
from datetime import datetime
import csv
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

def collect_feedback(name, email, feedback, image, status="Pending"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save the image with a secure filename
    image_filename = "No Image"
    if image.filename:
        image_filename = secure_filename(image.filename)
        image.save(os.path.join("uploads", image_filename))

    feedback_data = [timestamp, name, email, feedback, image_filename, status]
    feedback_file = "feedback.csv"  # Path to your CSV file

    if not os.path.isfile(feedback_file):
        with open(feedback_file, "w", newline="") as csvfile:
            fieldnames = ["Timestamp", "Name", "Email", "Feedback", "Image", "Status"]
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)

    with open(feedback_file, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(feedback_data)

@app.route("/", methods=["GET", "POST"])
def index():
    feedback_count = 0  # Initialize feedback count

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        feedback = request.form["feedback"]
        image = request.files["image"]

        if image.filename:
            image_filename = secure_filename(image.filename)
            image.save(os.path.join("uploads", image_filename))
        else:
            image_filename = "No Image"

        collect_feedback(name, email, feedback, image, status="Pending")

        feedback_count += 1  # Update feedback count

        return "Thank you for your feedback! Total feedbacks collected: {}".format(feedback_count)

    return render_template("index.html", feedback_count=feedback_count)

if __name__ == "__main__":
    app.run(debug=True)
