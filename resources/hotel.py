from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required


# hoteis = [

#     {
#         'hotel_id': "alpha",
#         'nome': 'Alpha Hotel',
#         'estrelas': 4.5,
#         'diaria': 420.50,
#         'cidade': 'São Paulo'

#     },
#     {
#         'hotel_id': "gama",
#         'nome': 'Alpha Hotel 1',
#         'estrelas': 4.3,
#         'diaria': 420.0,
#         'cidade': 'Rio de janeiro'

#     },
#     {
#         'hotel_id': "beta",
#         'nome': 'Alpha Hotel 2',
#         'estrelas': 4.0,
#         'diaria': 320.50,
#         'cidade': 'Curitiba'

#     }

# ]




class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}
        # return {'hoteis': hoteis}

class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="campo nome não pode deixar em branco")
    argumentos.add_argument('estrelas', type=float, required=True, help="the field 'estrlas' cannot be left blank.")
    argumentos.add_argument('diaria', type=float, required=True, help="the field 'diaria' cannot be left blank.")
    argumentos.add_argument('cidade', type=str, required=True, help="the field 'diaria' cannot be left blank.")

    def get(self, hotel_id):

        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404


    @jwt_required()
    def post(self, hotel_id):

        if HotelModel.find_hotel(hotel_id):
            return {'message': f'Já existe o hotel {hotel_id.upper()} cadastrado.'}, 400
            
      
        dados = self.argumentos.parse_args()
        # dados = Hotel.atributos.parse_args()


        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocorred trying to save hotel.'}, 500 # error interno servidor


        return hotel.json()

        # novo_hotel = HotelModel(hotel_id, **dados).json()
        # hoteis.append(novo_hotel)
        # return novo_hotel, 200


    @jwt_required()
    def put(self, hotel_id):
        '''
        Se não existir no banco de dados ele cria,
        Se existir no banco de dados ele atualiza
        '''
        # novo_hotel = HotelModel(hotel_id, **dados).json()
        dados = self.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        # hotel = self.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel() # salvando no banco de dados


            return hotel_encontrado.json(), 200 #ok


        hotel = HotelModel(hotel_id, **dados)

        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocorred trying to save hotel.'}, 500 # error interno servidor
        
        return hotel.json(), 201 #created criado
        

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An internal error ocorred trying to delete hotel.'}, 500 # error interno servidor
            
            return {'message': 'Hotel deleted.'}
        
        
        # global hoteis # global para referenciar a variavel de fora
        # hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'Hotel not found.'}, 404


        