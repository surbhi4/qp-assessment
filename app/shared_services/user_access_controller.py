from flask import request, jsonify, Blueprint
from app.shared_services.user_access_model import user_access_model
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.blocklist import BLOCKLIST

blp = Blueprint("Users", __name__)

obj = user_access_model()

@blp.route("/user/adduser", methods=['POST'])
@jwt_required()
def adduser():
    try:
        current_user = get_jwt_identity()
        if current_user['role'] == 'admin':
            data = request.json
            username = data.get('username')
            password = data.get('password')

            # Check if both username and password are provided
            if not username or not password:
                return jsonify({"error": "Both username and password are required"}), 400

            # Call your add_user function with the provided username and password
            obj.add_user(username, password)

            return jsonify({"message": f"User {username} added successfully"}), 201
        else:
            return jsonify({"error": "Only admins can add a user"}), 401
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

@blp.route("/user/login", methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        res = obj.user_data(username, password)
        return res
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

@blp.route("/user/logout", methods=['POST'])
@jwt_required()
def logout():
    try:
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "User logged out successfully"}
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500
