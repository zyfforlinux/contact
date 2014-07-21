from page import db


class contact(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(100),nullable=False)
	year = db.Column(db.Integer,nullable=False)
	sex = db.Column(db.String(10),nullable=False)
	job = db.Column(db.String(100),nullable=False)
	tel = db.Column(db.String(20),nullable=False)
	qq = db.Column(db.String(20),nullable=False)
	email = db.Column(db.String(50),nullable=False)
	def __init__(self,username,year,sex,job,tel,qq,email):
		self.username = username
		self.year = year
		self.sex = sex
		self.job = job
		self.tel = tel
		self.qq = qq
		self.email = email
	
	def __repr__(self):
		return "<%s >" %self.username


if __name__ == "__main__":
	db.create_all()
