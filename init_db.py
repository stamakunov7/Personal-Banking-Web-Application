import sqlite3

# Create the database
def create_db():
    con = sqlite3.connect('banking.db')
    c = con.cursor()
    
    # Create the tables
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 name TEXT NOT NULL, 
                 email TEXT NOT NULL UNIQUE)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                 id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 account_number TEXT NOT NULL, 
                 amount REAL NOT NULL, 
                 transaction_type TEXT NOT NULL CHECK (transaction_type IN ('deposit', 'withdrawal')))''')
    
    # Commit the changes
    con.commit()
    con.close()

# Run the function
if __name__ == '__main__':
    create_db()