# app/__init__.py
from flask import Flask
from flask_cors import CORS  # Import CORS
from .routes import main, socketio

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes
    app.config.from_object('config.Config')
    app.register_blueprint(main)
    socketio.init_app(app, cors_allowed_origins="*")  # Enable CORS for socket connections
    return app
