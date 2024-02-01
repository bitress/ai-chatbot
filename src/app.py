from flask import Flask, render_template, request, jsonify
import json
import nltk
from nltk.tokenize import word_tokenize
import random

app = Flask(__name__)


def preprocess_text(text):
    tokens = word_tokenize(text)
    return ' '.join(tokens)


def load_rules_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            rules = json.load(json_file)
    except FileNotFoundError:
        rules = []

    return rules


def save_rules_to_json(file_path, rules):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(rules, json_file, indent=2)


def add_rule(rules, questions, responses):
    new_rule = {"questions": questions, "responses": responses}
    rules.append(new_rule)
    return rules


def simple_chatbot(user_input, rules):
    preprocessed_input = preprocess_text(user_input)

    matched_rules = [rule for rule in rules if any(keyword in preprocessed_input for keyword in rule["questions"])]

    if matched_rules:
        selected_rule = random.choice(matched_rules)
        return random.choice(selected_rule["responses"])
    else:
        return ("I'm sorry, I couldn't understand your query. If you have a specific question, please provide more "
                "details.")


# Load rules from JSON
json_file_path = '../data/knowledge_base.json'
rules = load_rules_from_json(json_file_path)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    response = simple_chatbot(user_input, rules)

    return render_template('index.html', user_input=user_input, response=response)


@app.route('/teach', methods=['POST'])
def teach():
    user_input = request.form['user_input']
    new_questions = request.form['new_questions'].split(',')
    new_responses = request.form['new_responses'].split(',')

    # Add the new rule to the rules list
    rules = add_rule(rules, new_questions, new_responses)

    # Save the updated rules to the JSON file
    save_rules_to_json(json_file_path, rules)

    response = simple_chatbot(user_input, rules)

    return render_template('index.html', user_input=user_input, response=response)


if __name__ == '__main__':
    app.run(debug=True)
