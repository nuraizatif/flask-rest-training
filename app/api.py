from flask import Flask
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:masukaja@127.0.0.1/rest_training'

api = Api(app)
db = SQLAlchemy(app)

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

client_field = {
    'client_id': fields.Integer,
    'client_key': fields.String,
    'client_secret': fields.String,
    'status': fields.Boolean
}

class Clients(db.Model):
    client_id = db.Column(db.Integer, primary_key=True)
    client_key = db.Column(db.String(30), unique=True, nullable=False)
    client_secret = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Clients %r>' % self.client_id

class ClientsResource(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('status', type=bool, location='args')
        args = parser.parse_args()

        if args['p']==1:
            offset = 0
        else:
            offset = (args['p'] * args['rp']) - args['rp']

        qry = Clients.query.limit(args['rp']).offset(offset)
        rows = []
        for row in qry.all():
            rows.append(marshal(row, client_field))

        return rows, 200

class ClientResource(Resource):

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

api.add_resource(ClientsResource, '/clients')
api.add_resource(ClientResource, '/client', '/client/<int:id>')
api.add_resource(HeaderPeek, '/headers')

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=5000)