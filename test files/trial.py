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

# @app.route("/")
# def home():
#     return render_template("index.html")

@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/", methods=["POST"])
# def get_response():

#     if request.method == 'POST':
#         user_input = request.form.get("user_input")
#         response = get_response_from_input(user_input)
#         return render_template("index.html", user_input=user_input, bot_response=response)
#     else:
#         return render_template('index.html', user_input=user_input)
# @app.route("/get_input", methods=['POST'])
# def get_input(user_input):
#         user_input = request.form.get("user_input")

#         simple_responses = {
#             "hello": "Hi there!",
#             "how are you": "I'm doing well, thank you!",
#             "bye": "Goodbye! Have a great day!",
#             # Add more mappings as needed
#         }

    
#     # Check if the user input is in the simple_responses dictionary
#         response = simple_responses.get(user_input.lower())

#         if response:
#             return render_template("index.html", user_input=user_input, bot_response=response)
#         else:
#             return "I'm sorry, I didn't understand that."

def ai_facts():
    # Initialize an empty list to store the responses
    fax_list = []
    
    with open('D:\\63947\\Documents\\GitHub\\project_retake\\response_sheet.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        first_line = True
        for row in data:
            if not first_line:
                fax_list.append({
                    "ai_responses": row[0],
                })
            else:
                first_line = False

    return fax_list


def message_probability(
    user_message, recognised_words, user_response=False, required_words=[]
):
    # ... (Your existing message_probability function)
        message_certainty = 0
        has_required_words = True

    #     # Counts how many words are present in each predefined message
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
        
# def check_all_messgaes(message):
#         highest_prob_list = {}
#         ai_related = False
            
#         def response(bot_response, list_of_words, user_response=False, required_words=[], ai_keywords=['ai', 'artificial intelligence', 'machine learning', 'intelligent machines']):
#                 nonlocal highest_prob_list
#                 nonlocal ai_related
                
#                 highest_prob_list[bot_response] = message_probability(
#                 message, list_of_words, user_response, required_words
#             )
            
#                 for word in message:
#                     if word in ai_keywords:
#                         ai_related = True








@app.route("/get_response_from_input", methods=['POST'])
def get_response_from_input():
    
    user_input = request.form.get("user_input")
    # Your response generation logic based on user input
    response = ai_facts()
    return render_template("index.html", user_input=user_input, bot_response=response)






# Use app.app_context() to create tables within the application context
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
    



