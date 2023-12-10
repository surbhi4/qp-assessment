from flask import Flask
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
from app.admin.admin_controller import admin_controller_app
from app.shared_services import blp
from app.user import user_controller_app

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "SAFWYDFWDBVUBEUGEDYEUE893EUEKDNDNSDLSCF"

jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header,jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header,jwt_payload):
    return (
        {
            "description": "User has been logged out",
            "error": "token_revoked"
        },
        401
    )




app.register_blueprint(blp)
app.register_blueprint(admin_controller_app)
app.register_blueprint(user_controller_app)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3600)
