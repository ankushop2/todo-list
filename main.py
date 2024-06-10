from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.models.models import db
from app.routes.user_routes import user_bp
from app.routes.task_routes import task_bp
from app.config.config import Config
from flask_jwt_extended.exceptions import NoAuthorizationError, JWTDecodeError, WrongTokenError

def init_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    db.init_app(app)
    jwt = JWTManager(app)

    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(task_bp, url_prefix='/api/todo')


    with app.app_context():
        db.create_all()
    
    @app.errorhandler(NoAuthorizationError)
    def handle_no_authorization_error(e):
        return jsonify({"message": "Missing authorization header"}), 401

    @jwt.expired_token_loader
    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    @jwt.needs_fresh_token_loader
    @jwt.revoked_token_loader
    def jwt_custom_error(*args):
        return jsonify({"message": "Access Denied"}), 401

    
    return app

if __name__ == '__main__':
    app = init_app()
    app.run(host='0.0.0.0', port=5002)

