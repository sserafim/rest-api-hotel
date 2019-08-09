from flask_restful import Resource, reqparse
from models.usuario import UserModel


class User(Resource):
    # /usuarios/{user_id}
    def get(self, user_id):                   # -----------------Get por ID
        user = UserModel.find_user(user_id)
        if user:
            return(user.json())
        return {'message': 'Uusuário not found'}, 404

    def delete(self, user_id):
        user = delete.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An internal error ocurred trying to delete usuário.'}, 500
            return {'message': 'Usuário deleted'}
        return {'message': 'Usuário not found.'}, 404

class UserRegister(Resource):
    # /cadastro
    def  post(self):
        attr = reqparse.RequestParser()
        attr.add_argument('login', type=str, required=True, help='The field login cannot be left blank')
        attr.add_argument('senha', type=str , required=True, help="The senha cannot be left blank")

        dados = attr.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"message": "The login '{}' already exists".format(dados['login'])}

        user = UserModel(**dados)
        user.save_user()
        return{'message': 'User cread successfully'},201

        