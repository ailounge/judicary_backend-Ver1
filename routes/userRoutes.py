from flask import request, jsonify
from models.users import User
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from models.case import Case
from models.filters import Filters
from  datetime import datetime
from bson.objectid import ObjectId
from mongoengine.queryset.visitor import Q
import json

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



    @app.route('/createCase', methods=['POST'])
    @jwt_required()
    def create_case():
        try:
            print("POST request received for creating a new case with data:", request.json)
            data = request.json

            # Create a new Case document
            temp = User.objects.get(id=data.get('user_id')),
            print("temp" , temp)
            new_case = Case(
                user_id=User.objects.get(id=data.get('user_id')),  # Assuming user_id is provided in the request
                JudgeNames=data.get('JudgeNames', []),
                People=data.get('People', []),
                Organizations=data.get('Organizations', []),
                Locations=data.get('Locations', []),
                Dates={
                    'DateOfHearing': data.get('Dates', {}).get('DateOfHearing', ''),
                    'JudgmentDate': data.get('Dates', {}).get('JudgmentDate', ''),
                    'NotificationDate': data.get('Dates', {}).get('NotificationDate', ''),
                },
                CaseNumbers=data.get('CaseNumbers', []),
                Appellants=data.get('Appellants', []),
                Respondents=data.get('Respondents', []),
                Money=data.get('Money', []),
                FIRNumbers=data.get('FIRNumbers', []),
                ReferenceArticles=data.get('ReferenceArticles', []),
                ReferredCases=data.get('ReferredCases', []),
                ReferredCourts=data.get('ReferredCourts', []),
                AppealCaseNumbers=data.get('AppealCaseNumbers', []),
                AppealCourtNames=data.get('AppealCourtNames', []),
                CaseApproval=data.get('CaseApproval', ''),
                ExtractiveSummary=data.get('ExtractiveSummary', ''),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            new_case.save()  # Save the new case to the database
            
            new_judge_names = data.get('JudgeNames', [])
            new_locations = data.get('Locations', [])
            new_case_types = [data.get('CaseType')] if 'CaseType' in data else []  # Adjust based on actual data structure

            # Check if a Filters document already exists
            filters_doc = Filters.objects.first()
            if not filters_doc:
                # If not, create a new Filters document and save it
                Filters(
                    JudgeFilters=new_judge_names, 
                    CaseTypeFilters=new_case_types, 
                    LocationFilters=new_locations,
                    created_at=datetime.utcnow(),  # Set created_at to now
                    updated_at=datetime.utcnow()  # Set updated_at to now
                ).save()
            else:
                # Update the existing Filters document with new values and update updated_at field
                update_operations = {'updated_at': datetime.utcnow()}  # Prepare to update updated_at
                
                for judge_name in new_judge_names:
                    Filters.objects().update_one(add_to_set__JudgeFilters=judge_name, **update_operations)
                for location in new_locations:
                    Filters.objects().update_one(add_to_set__LocationFilters=location, **update_operations)
                for case_type in new_case_types:
                    Filters.objects().update_one(add_to_set__CaseTypeFilters=case_type, **update_operations)

            
            return jsonify(new_case.to_json()), 201  # Return the JSON representation of the new case with status code 201 (Created)
        except Exception as e:
            print("Error occurred:", str(e))
            return jsonify({'error': str(e), "status_code": 500}), 500  # Return error response with status code 500 if an error occurs

    @app.route('/getFilters', methods=['GET'])
    @jwt_required()
    def get_filters():
        try:
            # Attempt to retrieve the single Filters document
            filters_doc = Filters.objects.first()
            
            # If the document exists, return its JSON representation
            if filters_doc:
            # Convert the document to a dictionary
                data = filters_doc.to_mongo().to_dict()
                # Remove unwanted fields
                data.pop('created_at', None)
                data.pop('updated_at', None)
                data.pop("_id",None)
                # # Convert ObjectId to string
                # data['_id'] = str(data['_id'])

                # # Fix for any other ObjectId fields
                # for key, value in data.items():
                #     if isinstance(value, ObjectId):
                #         data[key] = str(value)

                return jsonify(data), 200
            else:
                # If no document is found, return a message
                return jsonify({"message": "No filters found"}), 404
            
        except Exception as e:
            print("Error occurred:", str(e))
            return jsonify({'error': str(e), "status_code": 500}), 500

    @app.route('/getCases', methods=['GET'])
    # @jwt_required()
    def get_cases():
        try:
            # Basic pagination setup
            page = int(request.args.get('page', 1))
            page_size = int(request.args.get('page_size', 10))

            # Initialize an empty query
            query = Q()

            # Retrieve filters and search string from request
            filters = request.args.get('filters')
            search_string = request.args.get('search', '')

            # Apply filters if they are provided
            if filters:
                filters_dict = json.loads(filters)
                for key, value in filters_dict.items():
                    # Add filter conditions for each key in the filters
                    query &= Q(**{f'{key}__in': value})

            # Apply search to the ExtractiveSummary if it is provided
            if search_string:
                search_query = Q(ExtractiveSummary__icontains=search_string)
                query &= search_query

            # Execute the filtered and/or search query with pagination
            cases_query = Case.objects(query).paginate(page=page, per_page=page_size)
            
            cases_list = []
            for case in cases_query.items:
                dates = case.Dates if case.Dates else Dates() 
                case_data = {
                    "_id": str(case.id),
                    "user": str(case.user_id.id) if case.user_id else '',
                    "JudgeNames": case.JudgeNames or [],
                    "People": case.People or [],
                    "Organizations": case.Organizations or [],
                    "Locations": case.Locations or [],
                    "Dates": {
                        "DateOfHearing": dates.DateOfHearing if dates.DateOfHearing else '',
                        "JudgmentDate": dates.JudgmentDate if dates.JudgmentDate else '',
                        "NotificationDate": dates.NotificationDate if dates.NotificationDate else '',
                    },
                    "CaseNumbers": case.CaseNumbers or [],
                    "Appellants": case.Appellants or [],
                    "Respondents": case.Respondents or [],
                    "Money": case.Money or [],
                    "FIRNumbers": case.FIRNumbers or [],
                    "ReferenceArticles": case.ReferenceArticles or [],
                    "ReferredCases": case.ReferredCases or [],
                    "ReferredCourts": case.ReferredCourts or [],
                    "AppealCaseNumbers": case.AppealCaseNumbers or [],
                    "AppealCourtNames": case.AppealCourtNames or [],
                    "CaseApproval": case.CaseApproval if case.CaseApproval else '',
                    "ExtractiveSummary": case.ExtractiveSummary if case.ExtractiveSummary else '',
                    "created_at": case.created_at.isoformat() if case.created_at else '',
                    "updated_at": case.updated_at.isoformat() if case.updated_at else '',
                }
                    
                
                cases_list.append(case_data)

            response = {
                'cases': cases_list,
                'total': cases_query.total,
                'pages': cases_query.pages,
                'page': page,
                'page_size': page_size,
            }

            return jsonify(response), 200
        except Exception as e:
            print("Error occurred:", str(e))
            return jsonify({'error': str(e), "status_code": 500})