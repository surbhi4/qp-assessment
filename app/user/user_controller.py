from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app
from app.user.user_model import user_model

user_controller_app = Blueprint('user_controller', __name__)

obj = user_model()

@app.route("/user/view_items", methods=['GET'])
@jwt_required()
def view_items():
    try:
        current_user = get_jwt_identity()
        if current_user['role'] == 'user':
            res = obj.all_user_model()
            return res
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@app.route("/user/book_items", methods=['POST'])
@jwt_required()
def book_items():
    try:
        current_user = get_jwt_identity()
        if current_user['role'] == 'user':
            data = request.json
            items_to_book = data.get('items', [])  # Assuming 'items' is a list of item names

            if not items_to_book:
                return jsonify({"message": "No items provided to book"}), 400

            booked_items = obj.book_user_items(items_to_book)

            return jsonify({"message": f"Items booked successfully: {booked_items}"}), 201
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
