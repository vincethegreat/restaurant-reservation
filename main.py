from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQLdb

app = Flask(__name__, static_url_path='/static')

app.secret_key = 'jezer-pala-sex'

def connection():
	try:
		conn = MySQLdb.connect(host="localhost",user="root",password="",db="db_aratan10")
		return conn
	except Exception as e:
		return str(e)
	
@app.route('/payment')
def payment():
	return render_template('payments.html')

@app.route('/login')
def login():
	return render_template('login.html')
@app.route('/signup')
def signup():
	return render_template('insert.html')
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/menus')
def menus():
    return render_template('menus.html')

@app.route('/booking_process', methods=['POST'])
def booking_process():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    date = request.form['date']
    time = request.form['time']
    number_of_guests = request.form['number_of_guests']

    conn = connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO reservations (name, email, phone, date, time, number_of_guests) VALUES (%s, %s, %s, %s, %s, %s)", (name, email, phone, date, time, number_of_guests))
    conn.commit()

    flash('Your reservation has been booked. Details: Name: {}, Email: {}, Phone: {}, Date: {}, Time: {}, Number of guests: {}'.format(name, email, phone, date, time, number_of_guests))

    return redirect(url_for('payment'))

@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
	conn = connection()
	cur = conn.cursor()
	cur.execute("SELECT * FROM reservations")
	reservations = cur.fetchall()
	return render_template('reservations.html', reservations=reservations)


#login session
@app.route('/login_process', methods=['GET', 'POST'])
def login_process():
    if request.method == "POST":
        uname = request.form['username']
        pw = request.form['password']

        conn = connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM tbl_users WHERE USERNAME = '{}' AND PASSWORD = '{}'".format(uname, pw))
        data = cur.fetchall()

        if data:
            session['username'] = uname
            return redirect('/')
        else:
            return "Login failed: username or password is incorrect"

#signup session
@app.route('/insert_process', methods=['GET', 'POST'])
def insert_process():
	if request.method == "POST":
		theID = request.form['user_id']
		uname = request.form['username']
		pw = request.form['password']

		conn = connection()
		cur = conn.cursor()
		cur.execute("INSERT INTO tbl_users VALUES('{}' , '{}' , '{}')".format(theID, uname, pw))
		conn.commit()

		return redirect("/login")


#fetching users to display in a table
@app.route('/display')
def display():
	conn = connection()
	cur = conn.cursor()
	cur.execute("SELECT * FROM tbl_users")
	data = cur.fetchall()

	return render_template('display.html', data = data)

#delete session
@app.route('/delete_process/<string:id>/')
def delete_process(id):

	conn = connection()
	cur = conn.cursor()
	cur.execute("DELETE FROM tbl_users WHERE USER_ID = '{}'".format(id))
	conn.commit()
	return redirect(url_for('display'))

@app.route('/reservation_delete/<string:id>/')
def reservation_delete(id):

	conn = connection()
	cur = conn.cursor()
	cur.execute("DELETE FROM reservations WHERE reservation_id = '{}'".format(id))
	conn.commit()
	return redirect(url_for('reservations'))

#update session
@app.route('/update_process_one/<string:id>/')
def update_process_one(id):
	conn = connection()
	cur = conn.cursor()
	cur.execute("SELECT * FROM tbl_users WHERE USER_ID = '{}'".format(id))
	data = cur.fetchone()
	return render_template('display_user.html', data = data)

@app.route('/update_process_two', methods=['POST'])
def update_process_two():
    user_id = request.form['user_id']
    username = request.form['username']
    password = request.form['password']
    
    conn = connection()
    cur = conn.cursor()
    cur.execute("UPDATE tbl_users SET USER_ID = '{}', USERNAME = '{}', PASSWORD = '{}' WHERE USER_ID = '{}'".format(user_id, username, password, user_id))
    conn.commit()
    return redirect(url_for('display'))

#Reservations Update
@app.route('/reservation_update_one/<string:id>/')
def reservation_update_one(id):
	conn = connection()
	cur = conn.cursor()
	cur.execute("SELECT * FROM reservations WHERE reservation_id = '{}'".format(id))
	data = cur.fetchone()
	return render_template('edit_reservation.html', data = data)

@app.route('/reservation_update_two', methods=['POST'])
def reservation_update_two():
    reservation_id = request.form['reservation_id']
    fname = request.form['fname']
    email = request.form['email']
    phone = request.form['phone']
    date = request.form['date']
    time = request.form['time']
    guests = request.form['guests']
    
    conn = connection()
    cur = conn.cursor()
    cur.execute("UPDATE reservations SET reservation_id = '{}', name = '{}', email = '{}', phone = '{}', date = '{}', time = '{}' , number_of_guests = '{}'    WHERE reservation_id = '{}'".format(reservation_id, fname, email, phone, date, time, guests))
    conn.commit()
    return redirect(url_for('reservations'))

if __name__ == '__main__':
	app.run(debug = True)
