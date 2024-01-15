from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def ai_facts():
    fax_list = []

    with open('D:\\63947\\Documents\\GitHub\\project_retake\\response_sheet.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        for row in data:
            fax_list.append({
                f"ai_responses{i}": value for i, value in enumerate(row)
            })

    return fax_list

def required_responses():
    needed_words = []

    with open('D:\\63947\\Documents\\GitHub\\project_retake\\required_words.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        for row in data:
            needed_words.append({
                f"required_responses{i}": value for i, value in enumerate(row)
            })

    return needed_words

def message_probability(user_input, recognised_words, user_response=False, required_words=[]):
    message_certainty = 0

    for word in user_input:
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words))

    has_required_words = all(word in user_input for word in required_words)
    
    if has_required_words or user_response:
        return int(percentage * 100)
    else:
        return 0



def get_dynamic_responses(user_input, required_words_list, response_list):
    user_input_lower = user_input.lower()

    for i, required_words_dict in enumerate(required_words_list):
        print(f"Processing required words {i + 1}:", required_words_dict)
        
        # Iterate over the key-value pairs in the dictionary
        for key, value in required_words_dict.items():
            question = value.lower()

            if question in user_input_lower:
                key = f"ai_responses{i}"
                if key in response_list[1]:
                    return response_list[1][key]
    print("")
    print('key')
    return "I don't know what you are talking about."


@app.route("/", methods=['POST', 'GET'])
def get_response_from_input():
    if request.method == 'POST':
        user_input = request.form.get("user_input")
        
        required_words_list = required_responses()
        response_list = ai_facts()

        # Call get_dynamic_responses to get the best match
        bot_response = get_dynamic_responses(user_input, required_words_list, response_list)

        return render_template("index.html", user_input=user_input, bot_response=bot_response)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)