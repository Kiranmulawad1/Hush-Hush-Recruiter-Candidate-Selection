from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey' 

candidate_responses = {}

users = [
    {"id": 1, "name": "Elon Musk", "q1_code":
"""
def fibonacci(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
    return memo[n]

print(fibonacci(6))
""",
"q2_code":
"""def find_missing_number(lst, n):
    expected_sum = n * (n + 1) // 2  # Sum of numbers from 1 to n
    actual_sum = sum(lst)
    return expected_sum - actual_sum

print(find_missing_number([1, 2, 4, 5, 6], 6))
""",
"q3_code": 
"""def is_balanced(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    
    for char in s:
        if char in pairs.values():
            stack.append(char)
        elif char in pairs.keys():
            if stack == [] or stack.pop() != pairs[char]:
                return False
    return stack == []

print(is_balanced("{[()]}"))
print(is_balanced("{[(])}"))
""", "email": "elon@x.com", "selected": False},
    {"id": 2, "name": "Jane Smith", "q1_code": "print('Hi')", "q2_code": "def run(): pass", "q3_code": "return False", "email": "jane.smith@example.com", "selected": False},
    {"id": 3, "name": "Bob Johnson", "q1_code": "print('Test')", "q2_code": "def calc(): pass", "q3_code": "return None", "email": "bob.johnson@example.com", "selected": False},
]

@app.route('/')
def home():
    """Homepage for selecting login"""
    return render_template('login.html')

@app.route('/candidate')
def index():
    """Candidate login route"""
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == 'elonmusk' and password == '123':
        session['user'] = 'candidate'
        return redirect(url_for('questions'))
    return redirect(url_for('index'))

@app.route('/questions')
def questions():
    if 'user' in session and session['user'] == 'candidate':
        return render_template('questions.html')
    return redirect(url_for('index'))

@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    if 'user' in session and session['user'] == 'candidate':
        
        candidate_responses['answer1'] = request.form['question1']
        candidate_responses['answer2'] = request.form['question2']
        candidate_responses['answer3'] = request.form['question3']
        return "Answers Submitted Successfully!"
    return redirect(url_for('index'))

@app.route('/tech_manager')
def tech_manager_login():
    """Tech Manager login route"""
    return render_template('tech_manager_login.html')

@app.route('/tech_manager_login', methods=['POST'])
def tech_manager_auth():
    username = request.form['username']
    password = request.form['password']
    if username == 'jeff' and password == '123':
        session['user'] = 'tech_manager'
        return redirect(url_for('view_responses'))
    return redirect(url_for('tech_manager_login'))

@app.route('/hr_manager', methods=['GET'])
def hr_manager_login():
    """HR Manager login route"""
    return render_template('hr_manager_login.html')

@app.route('/hr_manager_login', methods=['POST'])
def hr_manager_auth():
    username = request.form['username']
    password = request.form['password']
    if username == 'billgates' and password == '123':
        session['user'] = 'hr_manager'
        return render_template('hr_dashboard.html', users=users, responses=candidate_responses)

    return redirect(url_for('hr_manager_login'))

@app.route('/view_responses')
def view_responses():
    """Viewing user details and candidate responses"""
    if 'user' in session and session['user'] == 'tech_manager':
        return render_template('view_responses.html', users=users, responses=candidate_responses)
    return redirect(url_for('index'))

@app.route('/candidate/<int:user_id>')
def candidate_details(user_id):
    """New route to view individual candidate responses"""
    if 'user' in session and session['user'] == 'tech_manager':
        user = next((user for user in users if user['id'] == user_id), None)
        if user:
            return render_template('candidate_responses.html', user=user, responses=candidate_responses)
    return redirect(url_for('index'))

@app.route('/select_candidate/<int:user_id>', methods=['POST'])
def select_candidate(user_id):
    if 'user' in session and session['user'] == 'tech_manager':
        
        for user in users:
            if user['id'] == user_id:
                user['selected'] = True
                print(f"Candidate {user['name']} selected.")
                break
        return redirect(url_for('view_responses'))
    return redirect(url_for('index'))

@app.route('/send_mail/<int:user_id>', methods=['POST'])
def send_mail(user_id):
    if 'user' in session and session['user'] == 'hr_manager':
        selected_user = next((user for user in users if user['id'] == user_id), None)
        if selected_user:
            print(f"Sending mail to {selected_user['email']}.")
            return redirect(url_for('hr_manager_login', mail_sent=True))
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """Logout route"""
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/hr_logout')
def hr_logout():
    """Logout route"""
    session.pop('hr_manager', None)
    return render_template('hr_manager_login.html')

@app.route('/tech_logout')
def tech_logout():
    """Logout route"""
    session.pop('tech_manager', None)
    return render_template('tech_manager_login.html')
if __name__ == '__main__':
    app.run(debug=True)