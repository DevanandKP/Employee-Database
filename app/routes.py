from flask import render_template, request, redirect, url_for
from app import app
import sqlite3
from flask import g

# Define the path to the database file
DATABASE = 'database.db'

# Create a function to get the database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Create a function to close the database connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Initialize the database schema (run this once to create the 'employees' table)
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Initialize the database when the application starts
init_db()

# Routes for the application
@app.route('/')
def index():
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM employees')
    employees = cursor.fetchall()
    return render_template('index.html', employees=employees)

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']

        connection = get_db()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO employees (name, position) VALUES (?, ?)', (name, position))
        connection.commit()

        return redirect(url_for('index'))

    return render_template('add_employee.html')
