import json
import nltk
from nltk.tokenize import word_tokenize
import random


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

while True:
    user_input = input("You: ")

    if user_input.lower() == 'exit':
        # Save rules and exit when the user enters 'exit'
        save_rules_to_json(json_file_path, rules)
        print("Chatbot: Bye!")
        break

    response = simple_chatbot(user_input, rules)
    print("Chatbot:", response)

    # Ask the user if they want to teach the chatbot
    teach_chatbot = input("Do you want to teach me? (yes/no): ").lower()

    if teach_chatbot == 'yes':
        new_questions = input("Enter new questions (comma-separated): ").split(',')
        new_responses = input("Enter responses (comma-separated): ").split(',')

        # Add the new rule to the rules list
        rules = add_rule(rules, new_questions, new_responses)
