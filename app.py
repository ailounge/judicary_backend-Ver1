import os
from dotenv import load_dotenv
# flask imports
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask import request, jsonify, session

# Environment imports
import server_reloader



#rRoutes Imports
from routes.userRoutes import userRoutes
from routes.authRoutes import authRoutes

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Update the MONGODB_SETTINGS to use the provided connection string
# MongodbURLNew = os.getenv('MongodbURLNew')


app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb+srv://Alucard008:UiIhOdwPy1xuM8jy@judiciarycluster.4jhslpg.mongodb.net/Judiciary_Database?retryWrites=true&w=majority'
}


jwtSecretKey = os.getenv('jwtSecretKey')
# Set a secret key for your application
app.config['JWT_SECRET_KEY'] = jwtSecretKey
app.config['JWT_HEADER_NAME'] = 'Authorization'
# Optionally, configure other JWT settings
app.config['JWT_TOKEN_LOCATION'] = ['headers']


# Initialize JWTManager
jwt = JWTManager(app)

# Custom error handler for JWT errors
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({'error': 'Token has expired'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'error': 'Invalid token'}), 401

@jwt.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({'error': 'Unauthorized access'}), 401




# Initialize MongoEngine with the Flask application
db = MongoEngine()
db.init_app(app)
CORS(app) # prevent CORS errors

# Import and configure routes
authRoutes(app)
userRoutes(app)

# Run the Flask application
if __name__ == "__main__":
    # server_reloader.main(run_server,before_reload=lambda: print('Reloading code…'))
    app.run(debug=True)
