from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
import bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()



class User( db.Model ):
    """ User Model """

    __tablename__ = 'users'

    id = db.Column( db.Integer, primary_key = True, autoincrement = True )
    username = db.Column( db.String, nullable = False, unique = True )
    password = db.Column( db.String, nullable = False )
    email = db.Column( db.String, nullable = False )
    dob = db.Column( db.Date, nullable = True )
    profile_picture = db.Column( db.String, nullable = True )


    def __init__( self, username, password, email, dob, profile_picture ):
        """ Initalize attributes of the User Model """

        s = self
        s.username = username 
        s.password = password
        s.email = email
        s.dob = dob
        s.profile_picture = profile_picture

    def __repr__( self ):
        """ Representation method of User Model """

        s = self
        return f'User || { s.id } || { s.username } || { s.email } || { s.dob } || { s.profile_picture }'
    
    @classmethod
    def create_user( cls, username, password, email, dob, profile_picture ):
        """ Creates a new user instance and pushed that instance to the Users Table in Database """

        # Note this will also hash the user instance password and store it as a string

        hash_pw = bcrypt.generate_password_hash( password )
        hashed_pw = hash_pw.decode( 'utf-8' )
        new_user = User( username, hashed_pw, email, dob, profile_picture )
        db.session.add( new_user )
        db.session.commit()
    
    @classmethod 
    def login( cls, username, password ):
        """ Authenticate and authorize a user """

        user = User.query.filter_by( username = username ).first()
        if user and bcrypt.check_password_hash( user.password, password ):
            return user
        else:
            return False    
        
    

class Search( db.Model ):
    """ Search Model """

    __tablename__ = 'searches'

    id = db.Column( db.Integer, primary_key = True, autoincrement = True )
    term = db.Column( db.String, nullable = False )
    time = db.Column( db.String, nullable = False  )
    user_id = db.Column( db.ForeignKey( 'users.id' ) ) 

    user = db.relationship( 'User', backref = 'searches' )

    def __init__( self, term, time, user_id ):
        """ Initalizes attributes of the Search class """

        s = self
        s.term = term
        s.time = time
        s.user_id = user_id

    def __repr__( self ):
        """ Representation method of the Search class """

        s = self
        return f'Search || { s.term } || { s.time } || { s.user_id }'
    
    @classmethod
    def add_search( cls, term, time, user_id ):
        """ Adds Search instance to the Database """
        
        new_search = Search( term, time, user_id )
        db.session.add( new_search )
        db.session.commit()
    
    @classmethod 
    def delete_search( cls, term, time, user_id ):
        """ Removes a selected search from the Database """

        search = Search( term, time, user_id )
        db.session.delete( search );
        db.session.commit();


   



    

















def connect_db( app ):
    """ Connect to Database """

    db.app = app
    db.init_app( app )


