from flask import Flask, render_template, g, request, redirect, url_for
import sqlite3

# Create the Flask app
app = Flask(__name__)
DATABASE = 'banking.db'

# Database connection functions
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

# Close the database connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Routes
@app.route('/')
def index():
    db = get_db()
    cur = db.execute('SELECT * FROM users')
    users = cur.fetchall()
    return render_template('index.html', users=users)

@app.route('/submit-transaction', methods=['POST'])
def submit_transaction():
    account_number = request.form['accountNo']
    amount = request.form['amount']
    transaction_type = request.form['transactionType']
    
    # Validate the account number
    db = get_db()
    try:
        db.execute('INSERT INTO transactions (account_number, amount, transaction_type) VALUES (?, ?, ?)',
                   (account_number, amount, transaction_type))
        db.commit()
    except sqlite3.Error as e:
        return f"An error occurred: {e}", 500
    
    return redirect(url_for('index'))

# Add a route for the transactions page
@app.route('/transactions')
def transactions():
    db = get_db()
    cur = db.execute('SELECT * FROM transactions')
    transactions = cur.fetchall()
    return render_template('transactions.html', transactions=transactions)

# Add a route for the accounts page
@app.route('/accounts')
def accounts():
    # Placeholder for accounts functionality
    return "Accounts functionality coming soon. Please contact Dr. Joshua Eckroth (jeckroth@stetson.edu) for help, I am just a freshman."

# Add a route for the contact page
@app.route('/contact')
def contact():
    # Placeholder for contact functionality
    return "Contact functionality coming soon. Please contact Dr. Joshua Eckroth (jeckroth@stetson.edu) for help, I am just a freshman."

# Add a route for the add-user page
@app.route('/add-user', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    
    db = get_db()
    try:
        db.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        db.commit()
    except sqlite3.Error as e:
        return f"An error occurred: {e}", 500
    
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
