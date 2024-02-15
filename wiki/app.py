from flask import Flask, request, redirect, render_template, session, flash
from forms import SearchPagesForm, NewUserForm, LoginForm
from models import db, connect_db, User, Search
from datetime import datetime
import requests



app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhimasecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///wiki_2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True 


app.app_context().push()
connect_db( app )


search_pages_base = 'https://en.wikipedia.org/w/rest.php/v1/search/page?'
search_page_base = 'https://en.wikipedia.org/w/rest.php/v1/page/'



# Menu Routes -------------------------------------------->
@app.route( '/', methods = ['GET', 'POST'] )
def homepage():
    """ Routes to the applications homepage """

    user_id = session.get( 'user_id' ) 
    form = SearchPagesForm()

    if form.validate_on_submit():
        term = form.search_input.data
        time = datetime.now().isoformat()
        Search.add_search( term, time, user_id )
        res = requests.get( f'{ search_pages_base }', params = { 'q': term, 'limit': '25' })
        if( res ):
            data = res.json()
            pages = data['pages']
            return render_template( 'search-pages.html', form = form, data = data, pages = pages )
        else:
            return render_template( 'search-pages.html', form = form )
    else:
        return render_template( 'search-pages.html', form = form )



@app.route( '/menu/<term>', methods = ['GET', 'POST'] )
def menu_search( term ):
    """ Routes to results based on user search """



# User Routes --------------------------------------------->
@app.route( '/new-user', methods = ['GET', 'POST'] )
def new_user():
    """ Routes to create a new user form """

    form = NewUserForm() 

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        dob = form.dob.data
        profile_picture = form.profile_picture.data
        User.create_user( username, password, email, dob, profile_picture )
        flash( f'🥳Congratulations { username }, you have successfully created a new account!🥳' ) 
        return redirect( '/' )
    else:
        return render_template( 'new-user.html', form = form )
    


@app.route( '/user-login', methods = ['GET', 'POST'] )
def user_login():
    """ Routes to Login User Page """

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.login( username, password )
        if user:
            session[ 'user_id' ] = user.id
            flash( f'Welcome back { username }, hope you are doing well today!!!' )
            return redirect( '/' )
        else: 
            form.username.errors[ 'Invalid Username or Password' ]
        
    return render_template( 'user-login.html', form = form )



@app.route( '/user-logout' )
def user_logout():
    """ Routes to Logout user """

    session.pop( 'user_id' )
    return redirect( '/' )



@app.route( '/user/searches' )
def user_searches():
    """ Routes to display users recent search history """

    user = User.query.filter_by( id = session[ 'user_id' ]).first() 
    if user:
        searches = Search.query.filter_by( user_id = user.id ).all()
        print( searches )

    return render_template( 'search.html', searches = searches )



# Search Routes ---------------------------------------->

@app.route( '/search-pages', methods = ['GET', 'POST'] )
def search_pages():
    """ Routes to search pages based on user input """

    user_id = session.get( 'user_id' )
    form = SearchPagesForm()

    if form.validate_on_submit():
        term = form.search_input.data
        time = datetime.now().isoformat()
        Search.add_search( term, time, user_id )
        return render_template( 'search-pages.html', form = form )
    else:
        return render_template( 'search-pages.html', form = form )



@app.route( '/get-page/<title>', methods = ['GET', 'POST'] )
def get_page( title ):

    response = requests.get( f'{search_page_base}{title}/html' )
    html = response.text;

    return render_template( 'page.html', html = html, title = title )



@app.route( '/edit-searches', methods = [ 'GET', 'POST' ])
def edit_searches():

    user = User.query.filter_by( id = session[ 'user_id' ]).first()
    if( user ):
        searches = Search.query.filter_by( user_id = user.id ).all()

    return render_template( 'edit-search.html', searches = searches )

