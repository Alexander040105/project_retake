from flask import Flask, render_template, request
import csv

app = Flask(__name__)



def ai_facts():
    response_list = []

    with open('D:\\63947\\Documents\\GitHub\\project_retake\\response_sheet.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        for column in data:
            if len(column) > 0:  # Ensure there is data in the row
                response_list.append(column[0].strip())

    return response_list

def required_responses():
    required_words = []

    with open('D:\\63947\\Documents\\GitHub\\project_retake\\required_words.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        for column in data:
            if len(column) > 0:  # Ensure there is data in the row
                required_words.append(column[0].strip())

    return required_words

def get_dynamic_responses(user_input, required_words_list, response_list):
    user_input_lower = user_input.lower()

    for i, response in enumerate(response_list):
        print(f"Processing response {i + 1}:", response)

        if response.lower() in user_input_lower:
            print(f"Match found for {response}. Returning response.")
            return response

    print("No match found. User Input:", user_input_lower)
    print("")
    print("")
    print("Response List:", response_list)
    print("")
    print("")
    print("Returning Unknown.")
    return "Unknown"



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