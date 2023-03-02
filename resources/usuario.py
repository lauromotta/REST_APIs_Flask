from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required
import hmac


atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="campo login não pode deixar em branco")
atributos.add_argument('senha', type=str, required=True, help="campo senha não pode deixar em branco")


def safe_str_cmp(a: str, b: str) -> bool:
    """This function compares strings in somewhat constant time. This
    requires that the length of at least one string is known in advance.

    Returns `True` if the two strings are equal, or `False` if they are not.
    """
    if isinstance(a, str):
        a = a.encode("utf-8")  # type: ignore

    if isinstance(b, str):
        b = b.encode("utf-8")  # type: ignore

    return hmac.compare_digest(a, b)


class User(Resource):
    # /usuarios/user_id
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'user not found.'}, 404
     

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An internal error ocorred trying to delete user.'}, 500 # error interno servidor
            return {'message': 'user deleted.'}
 
        return {'message': 'user not found.'}, 404

class UserRegister(Resource):
    # /cadastro
    def post(self):

        dados = atributos.parse_args()
 
        if UserModel.find_by_login(dados['login']):
            # the login {dados["login"]} already exists.
            return {'message': f'The login {dados["login"]} já existi'}
        
        user = UserModel(**dados)
        user.save_user()
        # Usuário criado com sucesso
        return {'message': 'User created successfully!'}, 201


class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()   

        user = UserModel.find_by_login(dados['login'])

        # if user and safe_str_cmp(user.senha, dados['senha']):
        if user and safe_str_cmp(user.senha.encode('utf-8'), dados['senha'].encode('utf-8')):
            token_de_acesso= create_access_token(identity=user.user_id)
            return {'acess_token': token_de_acesso}, 200
        
        return {'message': 'THe username or password is incorrect.'}, 401

