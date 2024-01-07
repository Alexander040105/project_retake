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

def unkown():
    unkown_words = []

    with open('D:\\63947\\Documents\\GitHub\\project_retake\\required_words.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        first_line = True
        for row in data:
            if not first_line:
                unkown_words.append({
                    f"required_responses{i}": value for i, value in enumerate(row)
                })
            else:
                first_line = False

    return unkown_words


def message_probability(user_input, recognised_words, user_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_input:
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words))

    for word in required_words:
        if word not in user_input:
            has_required_words = False
            break

    
    if has_required_words or user_response:
        return int(percentage * 100)
    else:
        return 0

def get_dynamic_responses(message, required_words_list, response_list):
    highest_prob_list = {}
    ai_related = False
    response_list = ai_facts()

    for i, required_words in enumerate(required_words_list):
        print(f"Processing required words {i + 1}:", required_words)
        print("")
        response_probability = message_probability(
            message, required_words,user_response=True
        )

        print(f"Response probability for required words {i + 1}: {response_probability}")
        print("")
        key = f"ai_responses{i + 1}"
        highest_prob_list[key] = response_probability
        print("")
        print(f"Adding to highest_prob_list: {key}")
        print("")

    for word in message:
        if word in ["ai", "artificial intelligence", "machine learning", "intelligent machines"]:
            ai_related = True

    print("Debug - highest_prob_list:", highest_prob_list)

    if not highest_prob_list:
        return "Unknown"  

    best_match_key = max(highest_prob_list, key=highest_prob_list.get)
    best_match_list = [best_match_key]

    if ai_related is False:
        return "Unknown" if highest_prob_list[best_match_key] < 1 else best_match_list
    else:
        return "Unknown AI" if highest_prob_list[best_match_key] < 1 else best_match_list


# def get_dynamic_responses(message, required_words_list, response_list):
#     highest_prob_list = {}
#     ai_related = False

#     for i, fact in enumerate(response_list):
#         print(f"Processing fact {i + 1}:", fact)
        
#         response_probability = message_probability(
#             message, required_words_list[i], user_response=True
#         )

#         print(f"Response probability for fact {i + 1}: {response_probability}")

#         key = f"ai_responses{i + 1}"
#         highest_prob_list[key] = response_probability
#         print(f"Adding to highest_prob_list: {key}")

#     for word in message:
#         if word in ["ai", "artificial intelligence", "machine learning", "intelligent machines"]:
#             ai_related = True

#     print("Debug - highest_prob_list:", highest_prob_list)

#     best_match_key = max(highest_prob_list, key=highest_prob_list.get)
#     best_match_list = [best_match_key]
    
#     if ai_related is False:
#         return "Unknown" if highest_prob_list[best_match_key] < 1 else best_match_list
#     else:
#         return "Unknown AI" if highest_prob_list[best_match_key] < 1 else best_match_list
    

@app.route("/", methods=['POST', 'GET'])
def get_response_from_input():
    if request.method == 'POST':
        user_input = request.form.get("user_input")
        
        required_words_list = required_responses()
        response_list = ai_facts()

        response = get_dynamic_responses(user_input.split(), required_words_list, response_list)
        return render_template("index.html", user_input=user_input, bot_response=response)
    else:
        return render_template('index.html')
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)