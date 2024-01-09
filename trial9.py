from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def read_csv(file_path):
    response = []
    
    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            response.append(row[0])
            
            

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