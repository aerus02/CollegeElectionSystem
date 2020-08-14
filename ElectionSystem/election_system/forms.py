from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired()])
	password = PasswordField('Password',validators=[DataRequired()])
	submit = SubmitField('Login')


class AddUserForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired()])
	password = PasswordField('Password',validators=[DataRequired()])
	collegeID = StringField('CollegeID',validators=[DataRequired()])
	submit = SubmitField('Add User')




class AddCategoryForm(FlaskForm):
	name = StringField('Category Name',validators=[DataRequired()])
	submit = SubmitField('Add Category')


class AddCandidateForm(FlaskForm):
	candidate_name = StringField('Candidate Name',validators=[DataRequired()])
	collegeID = StringField('CollegeID    ',validators=[DataRequired()])
	category_name = StringField('Category Name',validators=[DataRequired()])	
	submit = SubmitField('Add Candidate')

class CurrentPollForm(FlaskForm):
	category_name = StringField('Category Name',validators=[DataRequired()])	
	submit = SubmitField('Current Poll')


class ProfileForm(FlaskForm):
	category_name = StringField('Category Name',validators=[DataRequired()])
	submit = SubmitField('View Profiles')

class AddVoteForm(FlaskForm):
	profileID = StringField('Candidate ID',validators=[DataRequired()])
	submit = SubmitField('Add Vote')
