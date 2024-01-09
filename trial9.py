from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def read_csv(file_path):
    response = []
    
    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            response.append(row[0])