from flask import request, jsonify, Blueprint
from app.admin.admin_model import admin_model
from flask_jwt_extended import jwt_required, get_jwt_identity

admin_controller_app = Blueprint('admin_controller', __name__)

obj = admin_model()

@admin_controller_app.route("/user/view_items", methods=['GET'])
@jwt_required()
def view_items():
    try:
        current_user = get_jwt_identity()
        if current_user['role'] == 'admin':
            res = obj.view_products()
            return jsonify(res), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@admin_controller_app.route("/user/add_item", methods=['POST'])
@jwt_required()
def add_user_item():
    try:
        current_user = get_jwt_identity()
        if current_user['role'] == 'admin':
            data = request.json
            params = {
                'name': data['name'],
                'price': data['price'],
                'inventory': data['inventory']
            }
            obj.add_items(params)
            return jsonify({"message": "Item added successfully"}), 201
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@admin_controller_app.route("/admin/remove_item/<item_name>", methods=['DELETE'])
@jwt_required()
def remove_item(item_name):
    try:
        current_user = get_jwt_identity()
        if current_user['role'] == 'admin':
            obj.delete(item_name)
            return jsonify({"message": f"Item {item_name} removed successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@admin_controller_app.route("/user/update_item", methods=['POST'])
@jwt_required()
def update_item():
    try:
        current_user = get_jwt_identity()
        if current_user['role'] == 'admin':
            data = request.json
            params = {
                'name': data['name'],
                'price': data['price'],
                'id': data['id']
            }
            obj.update_product(params)
            return jsonify({"message": "Item updated successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@admin_controller_app.route("/user/manage_inventory", methods=['POST'])
@jwt_required()
def manage_inventory():
    try:
        current_user = get_jwt_identity()
        if current_user['role'] == 'admin':
            data = request.json
            params = {
                'name': data['name'],
                'inventory': data['inventory']
            }
            obj.manage_inventory(params)
            return jsonify({"message": "Inventory managed successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
