from flask import Flask , render_template , request , redirect , url_for , flash
import sqlite3 as sql
import os

file_path = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)

# in the first run : in your url write after 5000/index to see index page  
@app.route('/index')
def index():
    con = sql.connect("contactDb.db")
    #
    con.row_factory = sql.Row
    cur=con.cursor()
    cur.execute("select * from users")
    data = cur.fetchall()
    con.close()
    return render_template('index.html', datas = data)

@app.route('/add_user', methods=['POST','GET'])
def add_user():
    if request.method ==  'POST':
        uname = request.form['uname']
        contact = request.form['contact']
        # 
        con = sql.connect("contactDb.db")
        cur = con.cursor()
        cur.execute("create table if not exists users (u_id integer primary key , u_name text , u_contact text)")
        cur.execute("insert into users (u_name,u_contact) values (?,?)",(uname,contact))
        con.commit()
        flash('User Added', 'success')
        con.close()
        return redirect(url_for("index"))
    return render_template('add_user.html')

@app.route('/edit_user/<string:uid>' , methods=['POST','GET'])
def edit_user(uid):
    #
    if request.method ==  'POST':
        uname = request.form['uname']
        contact = request.form['contact']
        con = sql.connect("contactDb.db")
        cur = con.cursor()
        cur.execute("update users set u_name=? , u_contact=? where u_id=?",(uname,contact,uid))
        con.commit()
        flash('User Updated', 'success')
        con.close()
        return redirect(url_for("index"))
    #create seconde con 
    con = sql.connect("contactDb.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from users where u_id =?",(uid,))
    # we need one user => using fetchone !
    data = cur.fetchone()
    con.close()
    return render_template('edit_user.html',datas = data)

@app.route('/delete_user/<string:uid>', methods=['GET'])
def del_user(uid):
    #
    con = sql.connect("contactDb.db")
    cur = con.cursor()
    cur.execute("delete from users where u_id =?",(uid,))
    con.commit()
    flash('User Deleted !', 'warning')
    con.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.secret_key='admin123'
    app.run(debug=True,port=5000)