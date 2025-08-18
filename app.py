from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Generate a random math question
def generate_question():
    operations = ['+', '-', '*', '/']
    op = random.choice(operations)
    if op == '+':
        a, b = random.randint(1, 50), random.randint(1, 50)
        answer = a + b
    elif op == '-':
        a, b = random.randint(1, 50), random.randint(1, 50)
        answer = a - b
    elif op == '*':
        a, b = random.randint(1, 12), random.randint(1, 12)
        answer = a * b
    else:
        b = random.randint(1, 12)
        answer = random.randint(1, 12)
        a = answer * b
        answer = a // b
    question = f"{a} {op} {b} = ?"
    return question, answer

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'score' not in session:
        session['score'] = 0
    if 'question' not in session or request.method == 'POST':
        session['question'], session['answer'] = generate_question()
    message = ''
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        try:
            if int(user_answer) == session['answer']:
                session['score'] += 1
                message = 'Correct!'
            else:
                message = 'Wrong!'
        except:
            message = 'Please enter a valid number.'
        if session['score'] >= 10:
            return redirect(url_for('win'))
        session['question'], session['answer'] = generate_question()
    return render_template('index.html', question=session['question'], score=session['score'], message=message)

@app.route('/win')
def win():
    score = session.get('score', 0)
    session.clear()
    return render_template('win.html', score=score)

if __name__ == '__main__':
    app.run(debug=True)
