from flask_restful import Resource, reqparse
from models.usuario import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from blacklist import BLACKLIST
import traceback


#global variables
attr = reqparse.RequestParser()
attr.add_argument('login', type=str, required=True,
                  help='The field login cannot be left blank')
attr.add_argument('senha', type=str, required=True,
                  help="The senha cannot be left blank")
attr.add_argument('email', type=str)
attr.add_argument('ativado', type=bool)


class User(Resource):
    # /usuarios/{user_id}
    def get(self, user_id):                   # -----------------Get por ID
        user = UserModel.find_user(user_id)
        if user:
            return(user.json())
        return {'message': 'Uusuário not found'}, 404

    @jwt_required
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An internal error ocurred trying to delete usuário.'}, 500
            return {'message': 'Usuário deleted'}
        return {'message': 'Usuário not found.'}, 404


class UserRegister(Resource):
    # /cadastro
    def post(self):

        dados = attr.parse_args()
        if not dados.get('email') or dados.get('email') is None:
            return{"message", "The field 'email' cannot be left blank."}, 404

        if UserModel.find_by_email(dados['email']):
            return {"message": "The email '{}' already exists".format(dados['email'])}, 400

        if UserModel.find_by_login(dados['login']):
            return {"message": "The login '{}' already exists".format(dados['login'])}, 400

        user = UserModel(**dados)
        user.ativado = False
        try:
            user.save_user()
            user.send_confirmation_email()
        except:
            user.delete_user()
            traceback.prin_exc()
            return {'messagte', 'An internal server error has ocurred.'}, 500
        return{'message': 'User created successfully!!!!!!!!!'}, 201


class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = attr.parse_args()

        user = UserModel.find_by_login(dados['login'])
        if user and safe_str_cmp(user.senha, dados['senha']):
            if user.ativado:
                token_de_acesso = create_access_token(identity=user.user_id)
                return {'access_token': token_de_acesso}, 200
            return{'message': 'User not confirmed.'}, 400
        return {'message': 'The username or password is incorrect'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti']  # Token identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully!!!'}, 200


class UserConfirm(Resource):
    # Raiz_do_site/confirmacao/{user_id}
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_user(user_id)

        if not user:
            return{"message": "User id '{}' not found".format(user_id)}, 404
        user.ativado = True
        user.save_user()
        return{"message": "User id'{}' confirmed successfully.".format(user_id)}, 200
