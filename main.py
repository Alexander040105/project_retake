from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class BotResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ai_response = db.Column(db.String(255), nullable = False)
    # ... add more columns as needed

    def __repr__(self):
        return f'<YourModel {self.id}>'

@app.route("/")
def home():
    return render_template("index.html")



# Use app.app_context() to create tables within the application context
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
    
def message_probability(
    user_message, recognised_words, user_response=False, required_words=[]
):
    # ... (Your existing message_probability function)
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or user_response:
        return int(percentage * 100)
    else:
        return 0

def get_response_from_input(user_input):
    # You can implement your logic to get the response based on user input here
    # For example, you can query the database for a relevant BotResponse
    # and return its AI response.
    # This is a placeholder implementation; adjust it based on your needs.

    # For now, let's assume you want a simple response for demonstration purposes.
        simple_responses = {
            "hello": "Hi there!",
            "how are you": "I'm doing well, thank you!",
            "bye": "Goodbye! Have a great day!",
            # Add more mappings as needed
        }

    # Check if the user input is in the simple_responses dictionary
        response = simple_responses.get(user_input.lower())

        if response:
            return response
        else:
            return "I'm sorry, I didn't understand that."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST", "GET"])
def get_response():
    user_input = request.form.get("user_input")
    response = get_response_from_input(user_input)
    return render_template("index.html", user_input=user_input, bot_response=response)