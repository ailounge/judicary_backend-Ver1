import os
import bcrypt
from flask import request, jsonify, session
from dotenv import load_dotenv
from models.users import User
from models.auth import Auth
from marshmallow import ValidationError
from datetime import datetime, timedelta
import jwt
from Validations.AuthSchema import AuthSchema
from Validations.LoginSchema import LoginSchema

#load  env variables
load_dotenv()
jwtSecertKey = os.getenv('jwtSecertKey')

def authRoutes(app):
    @app.route('/login', methods=['POST'])
    def login():
        try:
            data = request.json
            schema = LoginSchema()
            email = data.get('email')
            password = data.get('password')
            
            try:
                validated_data = schema.load(data)
            except ValidationError as err:
                return jsonify({'error': err.messages}), 400

            # Retrieve user from the database based on the provided email
            auth_user = Auth.objects(email=email).first()

            # Check if user exists and verify the password
            if auth_user and bcrypt.checkpw(password.encode('utf-8'), auth_user.password.encode('utf-8')):
                # Retrieve the associated user profile from the User collection
                user_profile = User.objects(auth_id=auth_user.id).first()

                # Generate JWT token with expiration time set to 24 hours from now
                expiration_time = datetime.utcnow() + timedelta(hours=24)
                token_payload = {
                    'sub': str(auth_user.id),  # Include the subject (user identifier) in the payload
                    'email': email,
                    'exp': expiration_time
                }
                token = jwt.encode(token_payload, jwtSecertKey, algorithm='HS256')
                
                # Include both auth_id and profile_id inside user_profile object
                user_profile_data = user_profile.to_json() if user_profile else {}
                user_profile_data['auth_id'] = str(auth_user.id) if auth_user else None
                user_profile_data['profile_id'] = str(user_profile.id) if user_profile else None
                
                # Construct response containing user profile and token
                response_data = {
                    'message': 'Logged in successfully!',
                    'token': token,
                    'user_profile': user_profile_data
                }
                return jsonify(response_data), 200
            else:
                return jsonify({'error': 'Invalid email or password' , "message" : "Login Failed"}), 401 # Use 401 for unauthorized
        except Exception as e:
            return jsonify({'error': str(e), 'status_code': 500}), 500


    #  No need for a logout route in backend as we are using JWT token for authentication
    # @app.route('/logout' , methods =['GET'])
    # def logout():
    #     try:
    #         session.pop('email', None)
    #         return jsonify({'message': 'Logged out successfully'}), 200
    #     except Exception as e:
    #         return jsonify({'error': str(e), 'status_code': 500}), 500

    @app.route('/register', methods=['POST'])
    def register():
        data = request.json
        register_schema = AuthSchema()
        # user_schema = UserSchema()

        try:
            # Validate incoming data for both Auth and User
            validated_auth_data = register_schema.load(data)
        except ValidationError as err:
            # Return validation errors
            return jsonify({'error': err.messages, 'status_code': 400}), 400

        try:
            # Check if the email is already registered
            if 'email' in validated_auth_data and Auth.objects(email=validated_auth_data['email']).first():
                return jsonify({'error': 'Email already exists'}), 400

            # print("validated", validated_auth_data)
            # Encrypt the password before saving
            password = validated_auth_data.pop('password')  # Remove 'password' from validated_auth_data
            encoded_password = password.encode(encoding='utf-8')
            hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt(15))

            # Create Auth document
            auth = Auth(email=validated_auth_data.get('email'), password=hashed_password)  # Use get() to handle if email is not present
            auth.save()

            # Create User document
            
            user_data = {'auth_id': auth.id}
            if 'firstName' in validated_auth_data:
                user_data['firstName'] = validated_auth_data['firstName']
            if 'lastName' in validated_auth_data:
                user_data['lastName'] = validated_auth_data['lastName']
            if 'gender' in validated_auth_data:
                user_data['gender'] = validated_auth_data['gender']
            if 'phone_number' in validated_auth_data:
                user_data['phone_number'] = validated_auth_data['phone_number']
            if 'cnic_number' in validated_auth_data:
                user_data['cnic_number'] = validated_auth_data['cnic_number']
            if 'organization' in validated_auth_data:
                user_data['organization'] = validated_auth_data['organization']
            if 'ntn_number' in validated_auth_data:
                user_data['ntn_number'] = validated_auth_data['ntn_number']
            if 'country' in validated_auth_data:
                user_data['country'] = validated_auth_data['country']
            if 'province' in validated_auth_data:
                user_data['province'] = validated_auth_data['province']
            if 'city' in validated_auth_data:
                user_data['city'] = validated_auth_data['city']
            if 'address' in validated_auth_data:
                user_data['address'] = validated_auth_data['address']
            if 'subscription' in validated_auth_data:
                user_data['subscription'] = validated_auth_data['subscription']


            user = User(**user_data)
            user.save()

            return jsonify({'message': 'User registered successfully'}), 201
        except Exception as e:
            return jsonify({'error': str(e), 'status_code': 500}), 500

