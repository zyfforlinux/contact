#coding=utf-8
from flask import Flask,request,url_for,g,render_template,session,redirect,flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail,Message
from threading import Thread
import config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:server@localhost/contact?charset=utf8"
app.config.from_object(config)
app.secret_key=app.config['SECERT_KEY']
db = SQLAlchemy(app)
mail = Mail(app)
from models import contact

@app.route("/")
@app.route("/index")
@app.route("/index/<int:page>",methods=['POST','GET'])
def index(page=1):
	data = contact.query.order_by(contact.username.desc()).paginate(page,10,False)
	current = data.items
	return render_template("index.html",pagination=data,contactdata=current)



@app.route("/admin",methods=['POST','GET'])
def admin():
	if request.method == "POST":
		if request.form['email'] == app.config['USERNAME'] and request.form['pass'] == app.config['PASS']:
			session['is_login'] = True
			session['username'] = request.form['email']
			return redirect(url_for("show"))
		else:
			flash("username or password error")
			return render_template("login.html")
	else:	
		return render_template("login.html")



@app.route("/admin/show")
@app.route("/admin/show/<int:page>")
def show(page=1):
	if session.has_key('is_login') and session['username'] == app.config['USERNAME']:
		data = contact.query.order_by(contact.username.desc()).paginate(page,10,False)
		current = data.items
		return render_template("list.html",pagination=data,contactdata=current)
	else:
		return redirect(url_for("admin"))

@app.route("/admin/add",methods=["POST","GET"])
def add():
	if session.has_key('is_login') and session['username'] == app.config['USERNAME']:
		if request.method == "POST":
			if request.form['inlineRadioOptions'] == "option1":
				sex = "男"
			else:
				sex = "女"
			con = contact(request.form['username'],request.form['year'],sex,request.form['job'],request.form['tel'],request.form['qq'],request.form['email'])
			db.session.add(con)
			db.session.commit()
			flash("add success")
			return render_template('add.html')
		else:
			return render_template("add.html")
	else:
		return redirect(url_for("admin"))


@app.route("/admin/del/<int:page>")
def delete(page):
	if session.has_key('is_login') and session['username'] == app.config['USERNAME']:
		status = contact.query.filter(contact.id==page).first()
		if status == None:
			flash("delete failue")
			return redirect(url_for('show'))
		db.session.delete(status)
		db.session.commit()
		flash("delete success")
		return redirect(url_for('show'))
	else:
		return redirect(url_for('admin'))


@app.route("/admin/update/<int:page>",methods=["POST","GET"])
def update(page):
	if session.has_key('is_login') and session['username'] == app.config['USERNAME']:
		if request.method == "POST":
			if request.form['inlineRadioOptions'] == "option1":
                        	sex = "男"
               		else:
                        	sex = "女"
			con = contact.query.get(page)
		#return con.id
			if con == None:
				flash("update error")
				return redirect(url_for("show"))
			con.username = request.form['username']
			con.year = request.form['year']
			con.sex = sex
			con.job = request.form['job']
			con.tel = request.form['tel']
			con.qq = request.form['qq']
			con.email = request.form['email']
                	db.session.commit()
                	flash("update success")
			return redirect(url_for("show"))
		else:
			contactdata = contact.query.get(page)
			if contactdata == None:
				return render_template("update.html")
			return render_template("update.html",data=contactdata)
	else:
		return render_template(url_for("admin"))

@app.route("/logout")
def logout():
	session.pop('is_login',None)
	session.pop('username',None)
	flash("You were log out")
	return redirect(url_for('admin'))
