from flask_restx import Namespace, Resource

order_namespace = Namespace('orders', description="Namespace for orders")


@order_namespace.route('orders/orders')
class OrderGetCreate(Resource):

    def get(self):

        """
            Get all the orders
        """

        pass

    def post(self):
        """
            Place a new orders
        """
        pass

@order_namespace.route('order/<int:order_id>')
class GetUpdateDelete(Resource):

    def get(self, order_id):
        """
            Retrieve an order by id
        """

    def put(self, order_id):
        """
            Update an order with id
        """

    def delete (self, order_id):
        """
            Delete an order by id
        """
    pass


@order_namespace.route('/users/<int:user_id>/order/<int:order_id>')
class GetSpecificOrderByUser(Resource):
    def get(self,user_id,order_id):
        """
            Get a user's specific  order
        """
        pass


@order_namespace.route('/users/<int:user_id>/orders/')
class UserOrders(Resource):

    def get(self,user_id):
        """
            Get all orders for a user
        """
        pass


@order_namespace.route('/order/status/<int:order_id>')
class UpdateOrderStatus(Resource):
    
    def patch(self,order_id):
        """
            Update an order status 
        """
        pass