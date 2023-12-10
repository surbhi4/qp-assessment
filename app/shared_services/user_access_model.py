import hashlib
import mysql.connector
from flask import abort
from flask_jwt_extended import create_access_token
from app.shared_services.config import dbconfig
from user_access_queries import UserAccessQueries

class UserAccessModel:
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host=dbconfig['host'], user=dbconfig['username'],
                                               password=dbconfig['password'], database=dbconfig['database'])
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print("Success: Connected to the database")
        except mysql.connector.Error as e:
            print(f"Error: {e}")

    def user_data(self, username, password):
        try:
            password_enc = hashlib.sha256(password.encode('utf-8')).hexdigest()
            user_info = self.verify_user(username, password_enc)

            if user_info:
                user_id = user_info['user_id']
                role = user_info['role']

                # Include role in the JWT payload
                access_token = create_access_token(identity=user_id, additional_claims={"role": role})

                return {
                    "access_token": access_token,
                    "user_id": user_id,
                    "role": role
                }

            abort(404, message="Username or password is incorrect")
        except Exception as e:
            return {"error": f"Error: {str(e)}"}

    def add_user(self, username, password):
        try:
            password_enc = hashlib.sha256(password.encode('utf-8')).hexdigest()
            add_user_query = UserAccessQueries.add_user(username, password_enc)
            self.cur.execute(add_user_query)
            self.con.commit()
            print("User added successfully")
        except Exception as e:
            return {"error": f"Error: {str(e)}"}

    def verify_user(self, username, password):
        try:
            verify_user_query = UserAccessQueries.verify_user(username, password)
            self.cur.execute(verify_user_query)
            result = self.cur.fetchone()
            return result if result else None
        except Exception as e:
            return {"error": f"Error: {str(e)}"}
