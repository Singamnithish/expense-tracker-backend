from flask import Flask, request, jsonify

app = Flask(__name__)

users = []
transactions = []
@app.route('/add_transaction')
#this function adds a new transaction(income/expense)
def add_transaction():
    username = request.args.get('username')
    amount = request.args.get('amount')
    t_type = request.args.get('type')

    if not username or not amount or not t_type:
        return "Missing data!"

    if t_type not in ['income','expense']:
        return "Type must be income or expense"
        
    transaction = {
        "username": username,
        "amount": amount,
        "type": t_type
    }

    transactions.append(transaction)

    return "Transaction added successfully"

@app.route('/transactions')
def view_transactions():
    return jsonify(transactions)
@app.route('/')
def home():
    return "Expense Tracker Running"

# View users
@app.route('/add_user')
def add_user():
    username = request.args.get("username")
    password = request.args.get("password")
    role = request.args.get("role")
    user = {
        "username": username,
        "password": password,
        "role": role
    }
    users.append(user)
    return "User added successfully"

@app.route('/login')
def login():
    username = request.args.get("username")
    password = request.args.get("password")

    for user in users:
        if user['username'] == username and user['password'] == password:
            return f"Login successfull! Role:{user['role']}"
        return "Invalid username or password"
@app.route('/users')
def get_users():
    username = request.args.get("username")

    for user in users:
        if user['username'] == username and user['role'] == 'admin':
            return jsonify(users)
    return "Access denied! only admin can view users"    

@app.route('/summary')
def summary():
    income = 0
    expense = 0

    for t in transactions:
        if t['type'] == 'income':
            income += float(t['amount'])
        elif t['type'] == 'expense':
            expense += float(t['amount'])

    balance = income - expense
    status = "profit" if balance >=0 else "Loss"

    return jsonify({
        "total_income": income,
        "total_expense": expense,
        "balance": balance,
        "status":status
    })
if __name__ == '__main__':
    app.run(debug=True)