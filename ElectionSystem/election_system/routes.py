from flask import render_template,flash,url_for,redirect,request,session,Response

from election_system.forms import LoginForm
from election_system import app,forms
from election_system.models import User,Votes,Candidates,Categories
from election_system import db


def checkLogin():
	userID = session['userID']
	if (not userID) or userID == -1:
		return true
	else :
		return false


def setResponseHeaders():
	response = Response()
	response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0') 
	return response


@app.route('/',methods=['GET'])
@app.route('/login',methods=['GET'])
def StartPageGet():
	form = LoginForm()
	return render_template('login.html',title = 'CES Login',form = form)


@app.route('/',methods=['POST'])
@app.route('/login',methods=['POST'])
def StartPagePost():
	form = LoginForm()
	setResponseHeaders()
	if form.validate_on_submit():
		username = form.username
		password = form.password
		users = User.query.filter_by(username = username.data).first()
		if(users and users.password == password.data):
			session['userID'] = users.id
			if users.id == 0:
				return redirect(url_for('HomeAdmin'))
			else :
				return redirect(url_for('HomeGet'))
			
		elif users:
			flash(f'Please enter correct password','warning')
		else :
			flash(f'Please enter correct username','warning')

	else:
		flash(f'Please enter vaild credentials','warning')

	return render_template('login.html',title = 'CES Login',form = form)


@app.route('/logout',methods=['GET'])
def LogoutPage():
	session['userID'] = -1
	return redirect(url_for('StartPageGet'))


@app.route('/home',methods=['GET'])
def HomeGet():
	setResponseHeaders()
	form = forms.ProfileForm()
	categories = Categories.query.all()
	print(session['userID'])
	return render_template('home.html',title='CES Home',form = form,categories = categories)



@app.route('/view-profiles',methods=['POST'])
def ViewProfilesPost():
	form = forms.ProfileForm()
	if form.validate_on_submit():
		category_name = form.category_name
		category = Categories.query.filter_by(name = category_name.data).first()
		if category:
			candidates = Candidates.query.filter_by(categoryID = category.id).all()
			form2 = forms.AddVoteForm()
			return render_template('profiles.html',title = 'CES Profiles',form = form2,candidates = candidates,category = category)
		else :
			flash(f'Please enter valid category_name','warning')

		
	else:
		flash(f'Please enter valid category details','warning')

	return render_template('home.html',title='CES Home',form = form)



@app.route('/profiles',methods=['POST'])
def ProfilesPost():
	form = forms.AddVoteForm()
	userID = session['userID']
	if (not userID) or userID == -1:
		return redirect(url_for('StartPageGet'))
	print(session['userID'])

	if(form.validate_on_submit()):
		categoryID = form.categoryID.data
		candidateID = int(form.profileID.data)
		categoryNumber = 'option'+str(categoryID+1)
		if categoryID and candidateID:
			votes = Votes.query.filter_by(id = userID).first()
			
			if votes and votes.categoryNumber > 0 :
				flash(f'Vote already registered','warning')
				return redirect(url_for('HomeGet'))

			db.session.delete(votes)
			votes.categoryNumber = candidateID+1
			db.session.add(votes)
			db.session.commit()
			flash(f'Vote registered successfully','success')
			return redirect(url_for('HomeGet'))



		else : 
			flash(f'Please enter valid profileID1','warning')

	else :
		flash(f'Please enter valid profileID2','warning')
	return redirect(url_for('HomeGet'))



@app.route('/home-admin',methods=['GET'])
def HomeAdmin():
	form1 = forms.AddCategoryForm()
	form2 = forms.AddCandidateForm()
	form3 = forms.AddUserForm()
	form4 = forms.CurrentPollForm()
	return render_template('home_admin.html',title = 'CES Home-Admin',form1 = form1,form2 = form2,form3 = form3,form4 = form4)


@app.route('/add-user',methods=['POST']) 
def DataEntry():
	form = forms.AddUserForm()
	if(form.validate_on_submit()):
		username = form.username
		password = form.password
		collegeID = form.collegeID
		db.session.add(User(username=username.data,password = password.data,collegeid = collegeID.data))
		db.session.commit()
		flash("User data Added successfully",'success')
		
	else :
		flash(f'Please enter valid user data','warning')
	return redirect(url_for('HomeAdmin'))


@app.route('/poll-count',methods=['POST'])
def CurrentPollCount():
	# categories = Categories.query.all()
	# for category in categories:
	# 	candidates = Candidates.query.filter_by(categoryID = category.id).all()
	# 	for candidate in candidates:
	# 		users = Polls.query.filter_by(option+str(category.id) = candidate.id)

	form = forms.CurrentPollForm()
	if(form.validate_on_submit()):
		category_name = form.category_name.data
		category = Categories.query.filter_by(name = category_name).first()
		if category:
			candidates = Candidates.query.filter_by(categoryID = category.id).all()
			votes = []
			for candidate in candidates:
				if category.id+1 == 1:
					users = Votes.query.filter_by(option1 = candidate.id+1).all()
				elif category.id+1 == 2:
					users = Votes.query.filter_by(option2 = candidate.id+1).all()
				elif category.id+1 == 3:
					users = Votes.query.filter_by(option3 = candidate.id+1).all()
				elif category.id+1 == 4:
					users = Votes.query.filter_by(option4 = candidate.id+1).all()
				elif category.id+1 == 5:
					users = Votes.query.filter_by(option5 = candidate.id+1).all()
				else:
					users = Votes.query.filter_by(option6 = candidate.id+1).all()
				votes.append(len(users))

			return render_template('currentpoll.html',title = 'CES Poll Count',category = category,candidates = candidates,votes = votes)

		else :
			flash(f'Please enter valid category_name','warning')

	return redirect(url_for('HomeAdmin'))


@app.route('/add-category',methods=['POST']) 
def CategoryEntry():
	form = forms.AddCategoryForm()
	if(form.validate_on_submit()):
		category_name = form.name
		db.session.add(Categories(name = category_name.data))
		db.session.commit()
		flash(f'Category data Added successfully','success')

	else :
		flash(f'Please enter valid category data','warning')
	return redirect(url_for('HomeAdmin'))



@app.route('/add-profile',methods=['POST']) 
def ProfileEntry():
	form = forms.AddCandidateForm()
	if(form.validate_on_submit()):
		candidate_name = form.candidate_name
		category_name = form.category_name
		collegeID = form.collegeID
		candidates = Candidates.query.filter_by(name = candidate_name.data)
		categories = Categories.query.filter_by(name = category_name.data).first()
		for candidate in candidates:
			if candidate.categoryID == categories.id:
				flash(f'Same data already exists','warning')
				return redirect(url_for('HomeAdmin'))
		if categories:
			candidate = Candidates(name = candidate_name.data,collegeID = collegeID.data,categoryID = categories.id)
			db.session.add(candidate)
			db.session.commit()
			flash(f'Profile data Added successfully','success')

		else:
			flash(f'Please enter valid category name','warning')


	else :
		flash(f'Please enter valid Profile data','warning')
	return redirect(url_for('HomeAdmin'))


	#logout  ,, login back check.,,error page

	#send data to display poll counts,send data to display i users' home,pprofiles page,different login for admin