from flask import Flask, render_template, request, redirect, session
import sqlite3
import time
import datetime

app = Flask(__name__)

# SQLite database configuration
DATABASE = 'database.db'

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (username TEXT, password TEXT)''')
    conn.commit()
    conn.close()

# Create the table when the application starts
create_table()

app.secret_key = 'True'

# Route for registration
@app.route('/register', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Store the user's data in the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()

        return redirect('/login')  # You can redirect to a success page or login page here

    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user's credentials are valid
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            # Set the user's username in the session
            session['username'] = user[0]
            return redirect('/home')  # Redirect to the home page after successful login
        else:
            return 'Invalid username or password'  # You can redirect to an error page here

    return render_template('login.html')


# Route for home
@app.route('/')
@app.route('/home')
def home():
    # Check if the user is logged in
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return render_template('home.html')  # Redirect to the login page if the user is not logged in


# Route for stopwatch
@app.route('/stopwatch')
def stopwatch():
    if 'start_time' not in session:
        session['start_time'] = time.time()

    elapsed_time = time.time() - session['start_time']
    elapsed_time = round(elapsed_time, 2)  # Round to 2 decimal places

    return render_template('stopwatch.html', elapsed_time=elapsed_time)


# Route for alarm clock
@app.route('/alarm', methods=['GET', 'POST'])
def alarm_clock():
    if request.method == 'POST':
        hour = int(request.form['hour'])
        minute = int(request.form['minute'])

        # Store the alarm time in the session
        session['alarm_time'] = datetime.time(hour=hour, minute=minute)

        return redirect('/alarm')

    # Check if the alarm time is set in the session
    if 'alarm_time' in session:
        current_time = datetime.datetime.now().time()
        alarm_time = session['alarm_time']

        if current_time >= alarm_time:
            # Perform the alarm action (e.g., play a sound, trigger a notification, etc.)
            message = "Alarm triggered!"
        else:
            message = "Alarm is set for {}.".format(alarm_time.strftime("%H:%M"))

        return render_template('alarmclock.html', message=message)
    else:
        return render_template('alarmclock.html')


# Route for timer
@app.route('/timer')
def timer():
    return render_template('timer.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
