from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

from api.utils import db
from api.orders.orders import Order, User


order_namespace = Namespace("orders", description="Namspace for orders")


order_model = order_namespace.model(
    "Order",
    {
        "id": fields.Integer(description="An Id"),
        "size": fields.String(
            description="Size of order",
            required=True,
            enum=["SMALL", "MEDIUM", "LARGE", "EXTRA_LARGE"],
        ),
        "order_status": fields.String(
            description="The status of the order",
            required=True,
            enum=["PENDING", "IN_TRANSIT", "DELIVERED"],
        ),
    },
)


@order_namespace.route("/orders")
class OrderGetCreate(Resource):
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self):
        
        orders = Order.query.all()
        return orders, HTTPStatus.OK

    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def post(self):
        """
        Create a new order
        """
        username = get_jwt_identity()

        current_user = User.query.filter_by(username=username).first()
        data = order_namespace.payload
        new_order = Order(
            size=data["size"],
            quantity=data["quantity"],
            flavour=data["flavour"],
        )

        new_order.customer = current_user
        db.session.add(new_order)
        db.session.commit()

        return new_order, HTTPStatus.CREATED


@order_namespace.route("/orders/<int:order_id>")
class GetUpdateDelete(Resource):

    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self, order_id):
        """
        Retirieve an order by id
        """

        order = Order.get_by_id(order_id)
        return order, HTTPStatus.OK


    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def put(self, order_id):
        """
        Update an order by id
        """

        order_to_update=Order.get_by_id(order_id)
        data=order_namespace.payload
        order_to_update.quantity=data['quantity']
        order_to_update.size=data['size']
        order_to_update.flavour=data['flavour']

        db.session.add()
        db.session.commit()

        return order_to_update, HTTPStatus.OK

    @jwt_required()
    @order_namespace.marshal_with(order_model)
    def delete(self, order_id):
        """
        Delete an order wit
        """

        order_to_delete=Order.get_by_id(order_id)

        db.session.delete(order_to_delete)
        db.session.commit()

        return order_to_delete, HTTPStatus.OK


@order_namespace.route("/user/<int:user_id>/order/<int:order_id>/")
class GetSpecificOrderByUser(Resource):
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self, user_id, order_id):
        """
        Get a user's specific order
        """
        user = User.get_by_id(user_id)
        order = Order.query.filter_by(id=order_id).filter_by(user=user).first()
        return order, HTTPStatus.OK


@order_namespace.route("/user/<int:user_id>/orders")
class UserOrders(Resource):

    @order_namespace.marshal_list_with(order_model)
    @jwt_required()
    def get(self, user_id):
        """
        Get all order by a specific
        """
        user = User.get_by_id(user_id)
        orders = user.orders
        return orders, HTTPStatus.OK


@order_namespace.route("/orders/status/<int:order_id>/")
class UpdateOrdersStatus(Resource):
    def patch(self, order_id):
        """
        Update an order's status
        """
        pass
