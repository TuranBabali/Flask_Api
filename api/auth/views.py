from flask_restx import Namespace, Resource, fields
from flask import request
from werkzeug.security import generate_password_hash

from api.models.users import User
from api.utils import db

auth_namespace = Namespace('auth', description="a namespace for authentication")

signup_model= auth_namespace.model(
    'SignUp', {
        'id': fields.Integer(),
        'username': fields.String(required=True,description="Username"),
        'email': fields.String(required=True,description="Email"),
        'password': fields.String(required=True,description="Password"), 
    }
)

user_model= auth_namespace.model(
    'User', {
        'id': fields.Integer(),
        'username': fields.String(required=True,description="Username"),
        'email': fields.String(required=True,description="Email"),
        'password': fields.String(required=True,description="Password"), 
        'is_active': fields.Boolean(description="This shows that User is activ"),
        'is_staff': fields.Boolean(description="This shows that User is a staff"),  # if user is a staff member
    }

)
 


@auth_namespace.route('/signup')
class Signup(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)  
    def post(self):

        """
            Create a new user account
        """
        data = request.get_json()

        backend_password= data['password']
        hash_olunmus_password= generate_password_hash(backend_password) 
        response = {'message': 'bomba kimidi'}
        if backend_password.isdigit():
            response={'message': 'Password should not contain any digits'}

        user= User(username=data['username'],email=data['email'],
                   password_hash=hash_olunmus_password)
        
        user.save( )
        return response


        
    




@auth_namespace.route('/login')
class Login(Resource):

    def post(self):
        """
            Generate a new JWT pair
        """
        pass
    


