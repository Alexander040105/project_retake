from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class BotResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ai_response = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<YourModel {self.id}>'

def ai_facts():
    fax_list = []

    with open('D:\\63947\\Documents\\GitHub\\project_retake\\response_sheet.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        first_line = True
        for row in data:
            if not first_line:
                fax_list.append({
                    f"ai_responses{i}": value for i, value in enumerate(row)
                })
            else:
                first_line = False

    return fax_list

def required_responses():
    needed_words = []

    with open('D:\\63947\\Documents\\GitHub\\project_retake\\required_words.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        first_line = True
        for row in data:
            if not first_line:
                needed_words.append({
                    f"required_responses{i}": value for i, value in enumerate(row)
                })
            else:
                first_line = False

    return needed_words

def message_probability(user_message, recognised_words, user_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    
    if has_required_words or user_response:
        return int(percentage * 100)
    else:
        return 0

# def check_all_messages(message):
#     highest_prob_list = {}
#     ai_related = False

#     # Your response generation logic
#     required_words_fact20 = ["ethical", "considerations"]

#     # fact_lists = ai_facts()

#     fact_lists = ai_facts()

#     if not all(isinstance(fact, dict) and "ai_responses" in fact for fact in fact_lists):
#         raise ValueError("Invalid format for fact_lists. It should be a list of dictionaries with 'ai_responses' key.")

#     for i, fact in enumerate(fact_lists):
#         if "ai_responses" not in fact:
#             raise ValueError(f"Missing 'ai_responses' key in the dictionary at index {i}.")

#         response_probability = message_probability(
#             message, required_words_fact20, user_response=True
#         )

#         highest_prob_list[fact["ai_responses"]] = response_probability

#         for word in message:
#             if word in ["ai", "artificial intelligence", "machine learning", "intelligent machines"]:
#                 ai_related = True

#     best_match_key = max(highest_prob_list, key=highest_prob_list.get)
#     best_match_list = [best_match_key]

#     if ai_related is False:
#         return "Unknown" if highest_prob_list[best_match_key] < 1 else best_match_list
#     else:
#         return "Unknown AI" if highest_prob_list[best_match_key] < 1 else best_match_list

global fact_lists 

fact_lists = ai_facts()


def check_all_messages(message, fact_lists):
    highest_prob_list = {}
    ai_related = False

    for i, fact in enumerate(fact_lists):
        print(f"Processing fact {i + 1}:", fact)
        
        response_probability = message_probability(
            message, required_words_fact(fact, i), user_response=True
        )

        print(f"Response probability for fact {i + 1}: {response_probability}")

        key = f"ai_responses{i + 1}"
        highest_prob_list[key] = response_probability
        print(f"Adding to highest_prob_list: {key}")

    for word in message:
        if word in ["ai", "artificial intelligence", "machine learning", "intelligent machines"]:
            ai_related = True

    print("Debug - highest_prob_list:", highest_prob_list)# Your response generation logic
    


    best_match_key = max(highest_prob_list, key=highest_prob_list.get)
    best_match_list = [best_match_key]
    
    if ai_related is False:
        return "Unknown" if highest_prob_list[best_match_key] < 1 else best_match_list
    else:
        return "Unknown AI" if highest_prob_list[best_match_key] < 1 else best_match_list

def required_words_fact(fact, index):
    # Customize the logic to extract required words for each response
    return [
        f"required_word{i}" for i in range(index + 1, index + 21)
    ]

# @app.route("/", methods=['POST', 'GET'])
# def get_response_from_input():
#     if request.method == 'POST':
        
#         required_words_list = required_responses()
#         response_list = ai_facts
        
#         for i, required_words in enumerate(required_words_list):
#             required_words = list(required_words.values())[0].split(',')
        
#         user_input = request.form.get("user_input")
#         # response = check_all_messages(user_input.split(), fact_lists)
#         if any(word.lower() in user_input.lower() for word in required_words):
#             response = response_list[i]
#             return render_template("index.html", user_input=user_input, bot_response=response)
#         else:
#             return 'Dili ko alam pre'
#             print("User Input:", user_input)
#             print("Required Words:", required_words)
#     else:
#         return render_template('index.html')
def get_dynamic_responses(user_input, required_words):
    response_list = []

    # Example 1: Check if any required word is present in the user input
    if any(word.lower() in user_input.lower() for word in required_words):
        response_list.append("Response A")

    # Example 2: Check for specific conditions in user input
    if "specific_condition" in user_input.lower():
        response_list.append("Response B")

    # Example 3: Use a default response if none of the conditions are met
    if not response_list:
        response_list.append("Default Response")

    return response_list




@app.route("/", methods=['POST', 'GET'])
def get_response_from_input():
    if request.method == 'POST':
        required_words_list = required_responses()
        user_input = request.form.get("user_input")

        for i, required_words_dict in enumerate(required_words_list):
            required_words = list(required_words_dict.values())[0].split(',')
            response_list = get_dynamic_responses(user_input, required_words)
            
            if response_list:
                # Assuming response_list is now a list of responses based on conditions
                response = response_list[i]
                return render_template("index.html", user_input=user_input, bot_response=response)
        
        # If no condition is met, return a default response
        return render_template("index.html", user_input=user_input, bot_response="Default response")

    else:
        return render_template('index.html')



# Use app.app_context() to create tables within the application context
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
