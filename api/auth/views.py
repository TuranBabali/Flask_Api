from  flask_restx import Namespace,Resource, fields
from flask import request
from  api.orders.orders import User 
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from api.utils import db
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity

auth_namespace = Namespace('auth', description="a namspace for authentication")


signup_model = auth_namespace.model(
    'SignUp',{
        'id': fields.Integer(),
        'username': fields.String(required=True, description="A username "),
        'email': fields.String(required=True, description="An email"),
        'password': fields.String(required=True, description="A password"),
        
    }
)

user_model=auth_namespace.model(
    'User',{'id': fields.Integer(),
        'username': fields.String(required=True, description="A username "),
        'email': fields.String(required=True, description="An email"),
        'password_hash': fields.String(required=True, description="A password"),
        'is_active': fields.Boolean(description="This shows that user is active"),
        'is_staff':fields.Boolean(description="Thiw show is activ admin")

    }
)

login_model = auth_namespace.model(
    'Login',{
        'email': fields.String(required=True,description="An email"),
        'password':fields.String(required=True, description="a Pssword")

    }
)





@auth_namespace.route('/signup')
class SignUp(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """
            Create a new user account 
        """
        data = request.get_json()
        
        new_user =User(
            username = data.get('username'),
            email = data.get('email'),
            password_hash =generate_password_hash(data.get('password')),
            
                    )

        db.session.add(new_user)
        db.session.commit()

        return new_user, HTTPStatus.CREATED

@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        

        data= request.get_json()
        email = data.get('email')
        password=data.get('password')
        user=User.query.filter_by(email=email).first()

        if (user is not None) and check_password_hash(user.password_hash,password):
            access_token= create_access_token(identity=user.username)
            refresh_token=create_refresh_token(identity=user.username)

            response={
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            return response, HTTPStatus.OK
        


@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        username=get_jwt_identity()
        access_token=create_access_token(identity=username)

        return {'access_token':access_token},HTTPStatus.OK