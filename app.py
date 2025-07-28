# app.py
from flask import Flask, render_template, request, redirect, url_for, session
import joblib
import os
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load ML model
model = joblib.load('career_model.pkl')

# Manual encoders (should match model training)
skill_encoder = {
    'programming': 3,
    'writing': 4,
    'design': 0,
    'math': 2,
    'biology': 1
}

interest_encoder = {
    'ai': 0,
    'journalism': 2,
    'art': 1,
    'engineering': 3,
    'medicine': 4
}

# Dummy user storage
users = {}

@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return "User already exists."
        users[username] = password
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid credentials."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        skill = request.form['skill'].strip().lower()
        interest = request.form['interest'].strip().lower()
        score = int(request.form['score'])

        skill_code = skill_encoder.get(skill, -1)
        interest_code = interest_encoder.get(interest, -1)

        if skill_code == -1 or interest_code == -1:
            return "Invalid skill or interest."

        prediction = model.predict([[skill_code, interest_code, score]])
        career = prediction[0]

        with open('predictions.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if os.stat('predictions.csv').st_size == 0:
                writer.writerow(['Skill', 'Interest', 'Score', 'Career'])
            writer.writerow([skill, interest, score, career])

        return render_template('result.html', career=career)
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
