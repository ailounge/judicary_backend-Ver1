from flask import request, jsonify
from models.users import User
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError



def userRoutes(app):
    @app.route('/users', methods=['GET'])
    @jwt_required()  # Protect the route with JWT authentication
    def query_records():
        try:
            # Get the identity of the current user from the JWT token
            current_user_email = get_jwt_identity()

            users = User.objects()

            # Construct list of user data including email and profile information
            user_list = []
            for user in users:
                user_data = {
                    'email': user.auth_id.email,  # Retrieve email from associated Auth document
                    'user_profile': {
                        'auth_id': str(user.auth_id.id),  # Convert ObjectId to string
                        'profile_id': str(user.id),  # Convert ObjectId to string
                        'firstName': user.firstName,
                        'lastName': user.lastName,
                        'gender': user.gender,
                        'phone_number': user.phone_number,
                        'cnic_number': user.cnic_number,
                        'organization': user.organization,
                        'ntn_number': user.ntn_number,
                        'country': user.country,
                        'province': user.province,
                        'city': user.city,
                        'address': user.address,
                        'subscription': user.subscription,
                        'created_at': user.created_at.isoformat(),
                        'updated_at': user.updated_at.isoformat()
                        # Add more fields as needed
                    }
                }
                user_list.append(user_data)

            return jsonify(user_list), 200

        except Exception as e:
            return jsonify({'error': str(e), "status_code": 500}), 500



    # @app.route('/createUser', methods=['POST'])
    # def create_record():
    #     try:
    #         print("POST request received with data:", request.json)
    #         data = request.json
    #         user = User(firstName=data['username'],lastName=data['lastName'], password=data['password'], email=data['email'], role=data['role'])
    #         user.save()
    #         return jsonify(user.to_json()), 201
    #     except Exception as e:
    #         print("Error occurred:", str(e))
    #         return jsonify({'error': str(e), "status_code": 500})

    # @app.route('/updateUserProfile', methods=['PUT'])
    # def update_record():
    #     try:
    #         print("PUT request received with data:", request.json)
    #         data = request.json
    #         user = User.objects(username=data['username']).first()
    #         if not user:
    #             return jsonify({'error': 'User not found'}), 404
    #         else:
    #             user.update(**data)
    #             return jsonify(user.to_json()), 200
    #     except Exception as e:
    #         print("Error occurred:", str(e))
    #         return jsonify({'error': str(e), "status_code": 500})

    # @app.route('/deleteUserProfile', methods=['DELETE'])
    # def delete_record():
    #     try:
    #         print("DELETE request received with data:", request.json)
    #         data = request.json
    #         user = User.objects(username=data['username']).first()
    #         if not user:
    #             return jsonify({'error': 'User not found'}), 404
    #         else:
    #             user.delete()
    #             return jsonify(user.to_json()), 200
    #     except Exception as e:
    #         print("Error occurred:", str(e))
    #         return jsonify({'error': str(e), "status_code": 500})
