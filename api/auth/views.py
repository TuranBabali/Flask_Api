from flask_restx import Namespace, Resource

auth_namespace = Namespace('auth', description="a namespace for authentication")



@auth_namespace.route('/signup')
class Signup(Resource):

    def post(self):

        """
            Create a new user account
        """
    
        pass



@auth_namespace.route('/login')
class Login(Resource):

    def post(self):
        """
            Generate a new JWT pair
        """
        pass
    


