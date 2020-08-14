from election_system import db



class User(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	username = db.Column(db.String(15),unique = True,nullable = False)
	password = db.Column(db.String(15),nullable = False)
	collegeid = db.Column(db.String(12),unique = True,nullable = False)

	def __repr__(self):
		return f"User('{self.id}','{self.username}','{self.password}','{self.collegeID}')"

class Votes(db.Model):#maximum categories be  to be 6
	id = db.Column(db.Integer,primary_key = True)
	option1 = db.Column(db.Integer,default = 0)	
	option2 = db.Column(db.Integer,default = 0)
	option3 = db.Column(db.Integer,default = 0)
	option4 = db.Column(db.Integer,default = 0)
	option5 = db.Column(db.Integer,default = 0)
	option6 = db.Column(db.Integer,default = 0)


	def __repr__(self):
		return f"Votes('{self.id}','{self.option1}','{self.option2}','{self.option3}','{self.option4}','{self.option5}','{self.option6}')"


class Candidates(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	categoryID = db.Column(db.Integer,nullable = False,default = 1)
	name = db.Column(db.String(15),nullable = False)
	collegeID = db.Column(db.String(15),nullable = False)

	def __repr__(self):
		return f"Candidates('{self.id}','{self.categoryID}','{self.name}','{self.collegeID}')"

class Categories(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	name = db.Column(db.String(15),nullable = False,unique = True)

	def __repr__(self):
		return f"Categories('{self.id}','{self.name}')"
