from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def sims_cheatlist():
    cheats = []
    with open('D:\\63947\\Documents\\GitHub\\project_retake\\response_sheet.csv', 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            cheats.append(row[0]) 
            
    return cheats





@app.route("/", methods=['POST'])
def put_cheats():
    sims_cheats = sims_cheatlist()
    return render_template("sims.html")