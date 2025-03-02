from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_key'

# ✅ Default Home Route - Redirect to Register Page
@app.route('/')
def index():
    return redirect('/register')  # Redirects to registration page

# Database Connection
def connect_db():
    return sqlite3.connect('database.db')

# Home Page
@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect('/login')

# Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        dept = request.form['department']
        year = request.form['year']
        section = request.form['section']
        password = request.form['password']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, dept, year, section, password) VALUES (?, ?, ?, ?, ?)",
                       (name, dept, year, section, password))
        conn.commit()
        conn.close()
        return redirect('/login')

    return render_template('register.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE name=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect('/home')
        else:
            return "Login Failed"

    return render_template('login.html')

# Logout Page
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/exit')

# Exit Page
@app.route('/exit')
def exit():
    return render_template('exit.html')

if __name__ == '__main__':
    app.run(debug=True)
