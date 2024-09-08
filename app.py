from flask import Flask, request, jsonify, render_template
import pandas as pd
import nltk
import re
import os

nltk.download('punkt')  # Download the punkt tokenizer

# Initialize Flask app
app = Flask(__name__)

# Load the judge data from the CSV file
data = pd.read_csv('supreme_judge.csv')  # Update path if necessary

# Function to get details about a specific judge
def get_judge_details(judge_name):
    judge_row = data[data['Name of the Judge'].str.contains(judge_name, case=False)]
    print(f"Searching for judge: {judge_name}")
    print(f"Matching rows: {judge_row}")  # Debugging statement
    
    if judge_row.empty:
        return "Sorry, I couldn't find any judge by that name."
    
    judge_info = judge_row.iloc[0]
    return (f"Judge: {judge_info['Name of the Judge']}\n"
            f"Date of Appointment: {judge_info['Date of Appointment']}\n"
            f"Date of Retirement: {judge_info['Date of Retirement']}\n"
            f"Remarks: {judge_info['Remarks']}\n"
            f"Parent High Court: {judge_info['Parent High Court']}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    print(f"User input: {user_input}")  # Debugging statement
    response = chatbot_response(user_input)
    return jsonify({'response': response})

def chatbot_response(user_input):
    tokens = nltk.sent_tokenize(user_input.lower())  # Split into sentences
    print(f"Tokenized input: {tokens}")  # Debugging statement
    for sentence in tokens:
        judge_pattern = r"(?:Justice\s)?([A-Za-z.\s]+)"
        match = re.search(judge_pattern, sentence)
        if match:
            judge_name = match.group(1).strip()
            print(f"Extracted judge name: {judge_name}")  # Debugging statement
            return get_judge_details(judge_name)
    return "I'm sorry, I couldn't find any judge by that name."

if __name__ == '__main__':
    app.run(debug=True)
