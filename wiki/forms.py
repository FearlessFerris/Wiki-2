from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, FileField, SubmitField, DateField
from wtforms.validators import InputRequired, Optional, Email, EqualTo



# Search Forms ------------------------------------>
class SearchPagesForm( FlaskForm ):
    """ Search Pages Form """

    search_input = StringField( 'Search', render_kw = { 'placeholder': 'Something cool is loading...'})



# User Forms -------------------------------------->
class NewUserForm( FlaskForm ):
    """ Create New User Form """

    username = StringField( 'Username:', validators = [ InputRequired ( message = 'Username is required!' ) ], render_kw = { 'placeholder': 'Username' })
    password = PasswordField( 'Password:', validators = [ InputRequired ( message = 'Password is required!' ), EqualTo ( 'verify_password', message = 'Passwords must match!' ) ], render_kw = { 'placeholder': 'Password' })
    verify_password = PasswordField( 'Verify Password:', render_kw = { 'placeholder': 'Verify Password' } )
    email = EmailField( 'Email:', validators = [ InputRequired ( message = 'Email is required!' ), Email() ], render_kw = { 'placeholder': 'Email' })
    dob = DateField( 'Date of Birth:', validators = [ Optional() ], render_kw = { 'placeholder': 'Date of Birth' } )
    profile_picture = FileField( 'Profile Picture:', validators = [ Optional () ])



class LoginForm( FlaskForm ):
    """ User Login Form """

    username = StringField( 'Username:', validators = [ InputRequired ( message = 'Username is required!' ) ], render_kw = { 'placeholder': 'Username' })
    password = PasswordField( 'Password:', validators = [ InputRequired ( message = 'Password is required!' ) ], render_kw = { 'placeholder': 'Password' })
