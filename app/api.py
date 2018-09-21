from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse

app = Flask(__name__)
api = Api(app)

clients = [
    {
        "client_id": 1,
        "client_key": "CLIENT01",
        "client_secret": "SECRET01",
        "status": True
    },
    {
        "client_id": 2,
        "client_key": "CLIENT02",
        "client_secret": "SECRET01",
        "status": True
    },
    {
        "client_id": 3,
        "client_key": "CLIENT03",
        "client_secret": "SECRET03",
        "status": True
    },
    {
        "client_id": 4,
        "client_key": "CLIENT04",
        "client_secret": "SECRET04",
        "status": False
    },
    {
        "client_id": 5,
        "client_key": "CLIENT05",
        "client_secret": "SECRET05",
        "status": False
    }
]

class Clients(Resource):

    def get(self):
        return clients

class Client(Resource):

    def get(self, id):
        for client in clients:
            if client['client_id'] == id:
                return client, 200
        
        return {'message': 'NOT_FOUND'}, 404
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_id', type=int, help='Client id must be an integer',	location='json', required=True)
        parser.add_argument('client_key', location='json', required=True)
        parser.add_argument('client_secret', location='json', required=True)
        parser.add_argument('status', type=bool, location='json')
        args = parser.parse_args()

        nuclient = {'client_id': args['client_id'], 'client_key': args['client_key'], 'client_secret': args['client_secret'], 'status': args['status']}

        clients.append(nuclient)
        
        return nuclient, 200

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='json', required=True)
        parser.add_argument('client_secret', location='json', required=True)
        parser.add_argument('status', type=bool, location='json')
        args = parser.parse_args()

        for idx, client in enumerate(clients):
            if client['client_id'] == id:
                changes = {'client_id': client['client_id'], 'client_key': args['client_key'], 'client_secret': args['client_secret'], 'status': args['status']}
                clients[idx] = changes
                return changes, 200
        
        return {'message': 'NOT_FOUND'}, 404
    
    def delete(self, id):
        for idx, client in enumerate(clients):
            if client['client_id'] == id:
                clients.pop(idx)
                return {'message': 'DELETED'}, 200
        
        return {'message': 'NOT_FOUND'}, 404

class HeaderPeek(Resource):
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('User-Agent', location='headers')
        parser.add_argument('X-CustomHeader', location='headers')
        args = parser.parse_args()
        return {'headers': args}

api.add_resource(Clients, '/clients')
api.add_resource(Client, '/client', '/client/<int:id>')
api.add_resource(HeaderPeek, '/headers')

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=5000)