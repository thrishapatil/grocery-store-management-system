from flask import Flask,render_template,url_for,session,request,redirect
import mysql.connector
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='grocerydb'
    )

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['is_admin'] = user['is_admin']
            return redirect(url_for('admin' if user['is_admin'] else 'shop'))
    return render_template('login.html')

@app.route('/admin')
def admin():
    if session['is_admin']==True:
        return render_template('admin.html')
    else:
        return redirect(url_for('login'))


@app.route('/shop',methods=['GET','POST'])
def shop():
    if request.method=='POST':
        # item_quantity=request.form[]
        a = request.form['quantityapple']
        print(f"apple quantity is {a}")
        g = request.form['quantitygrape']
        print(f"grape quantity is {g}")
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM items ')
    user = cursor.fetchall()
    cursor.execute('SELECT name,price from items')
    items =cursor.fetchall()
    total = sum(item['price'] for item in items)
    conn.close()

    return render_template('shop.html',items=user,item=items,total=total)

if __name__ == '__main__':
    app.run(debug=True)
