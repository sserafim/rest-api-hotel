from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'estrelas': 4.3,
        'diaria': 450.30,
        'cidade': 'Osasco'
    },
    {
        'hotel_id': 'copacabana',
        'nome': 'copacabana Hotel',
        'estrelas': 4.3,
        'diaria': 920.30,
        'cidade': 'Rio de Janeiro'
    },
    {
        'hotel_id': 'ibis',
        'nome': 'ibis Hotel',
        'estrelas': 4.3,
        'diaria': 520.30,
        'cidade': 'Santa Catarina'
    },
    {
        'hotel_id': 'feiticeira',
        'nome': 'feiticeira Hotel',
        'estrelas': 4.3,
        'diaria': 420.30,
        'cidade': 'São Paulo'
    }
]

# -----------------------------------------------------------------------------------------------


class Hoteis(Resource):
    def get(self):            # --------------------- Get All
        return {'hoteis': hoteis}

# -----------------------------------------------------------------------------------------------


class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):                   # -----------------Get por ID
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return(hotel)
        return {'message': 'Hotel not found'}, 404

    def post(self, hotel_id):                  # -----------------------Post
        if HotelModel.find_hotel(hotel_id):
            return {'message': 'Hotel id '"{}"' already exists.'.format(hotel_id)}, 400

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json()

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json(), 201

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.delete_hotel()
            return {'message': 'Hotel deleted'}
        return {'message': 'Hotel not found.'}, 404
