from flask_restful import Resource,reqparse
from models.user import UserModel

class UserRegister(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument(
        'username',
        type = str,
        required = True,
        help = "This field can not be blank"
    )

    parse.add_argument(
        'password',
        type = str,
        required = True,
        help = "This field can not be lank"
    )

    def post(self):
        data = UserRegister.parse.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message":"User already exist"}, 400 #400 bad request status code
        else:
            user = UserModel(**data)
            user.save_to_db()
            return {"message":"User create successfully."}, 201