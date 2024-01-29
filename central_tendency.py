from flask import Flask, render_template, request
import csv

app = Flask(__name__)

#algorithm
def compute_central_tendency():
    number_of_items = len(user_numbers)
    sorted_numbers = sorted(user_numbers)
    
    converted_to_int = [int(x) for x in user_numbers]
    mean = sum(converted_to_int)/int(number_of_items)
    print('The mean is ' + str(mean))
    
    if number_of_items % 2 == 1:
        median = sorted_numbers[number_of_items//2]
        print('The median is ' + str(median))
    else:
        median1 = sorted_numbers[(number_of_items//2) - 1]
        median2 = sorted_numbers[number_of_items//2]
        print('The median is ' + str(median1) + ' and ' + str(median2))




@app.route("/", methods=['POST'])
def central_tendencies_input():
    user_numbers = []
    numbers = [value.strip() for value in user_input.split(',')]
    user_numbers = user_numbers + numbers
    
    if request.method == 'POST':
        user_input = request.form.get("user_input")
        return render_template("sims.html", user_input=user_input)
    
    