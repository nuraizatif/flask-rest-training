from flask import Flask
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, desc
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:masukaja@127.0.0.1/rest_training'
app.config['SQLALCHEMY_ECHO'] = True

api = Api(app)
db = SQLAlchemy(app)

client_field = {
    'client_id': fields.Integer,
    'client_key': fields.String,
    'client_secret': fields.String,
    'status': fields.Boolean
}

class Client(db.Model):
    __tablename__ = "clients"
    client_id = db.Column(db.Integer, primary_key=True)
    client_key = db.Column(db.String(30), unique=True, nullable=False)
    client_secret = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Client %r>' % self.client_id

class ClientsResource(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('status', location='args', help='invalid status', choices=('true','false','True','False'))
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=('client_id','client_key','status'))
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc','asc'))
        args = parser.parse_args()

        if args['p']==1:
            offset = 0
        else:
            offset = (args['p'] * args['rp']) - args['rp']

        qry = Client.query

        if args['status']=="True".lower():
            qry_1 = qry.filter_by(status=True)
        elif args['status']=="False".lower():
            qry_1 = qry.filter_by(status=False)
        else:
            qry_1 = qry

        if args['orderby']=='client_id':
            if args['sort']=='desc':
                qry_2 = qry_1.order_by(desc(Client.client_id))
            else:
                qry_2 = qry_1.order_by(Client.client_id)
        elif args['orderby']=='client_key':
            if args['sort']=='desc':
                qry_2 = qry_1.order_by(desc(Client.client_key))
            else:
                qry_2 = qry_1.order_by(Client.client_key)
        elif args['orderby']=='status':
            if args['sort']=='desc':
                qry_2 = qry_1.order_by(desc(Client.status))
            else:
                qry_2 = qry_1.order_by(Client.status)
        else:
            qry_2 = qry_1

        rows = []
        for row in qry_2.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, client_field))

        return rows, 200

class ClientResource(Resource):

    def get(self, id):
        qry = Client.query.get(id)
        if qry is not None:
            return marshal(qry, client_field), 200
        return {'status': 'NOT_FOUND'}, 404
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='json', required=True)
        parser.add_argument('client_secret', location='json', required=True)
        parser.add_argument('status', type=bool, location='json')
        args = parser.parse_args()

        obj = Client(client_key=args['client_key'], client_secret=args['client_secret'], status=args['status'])
        db.session.add(obj)
        db.session.commit()

        app.logger.debug('DEBUG : %s', obj)
        
        return marshal(obj, client_field), 200

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='json', required=True)
        parser.add_argument('client_secret', location='json', required=True)
        parser.add_argument('status', type=bool, location='json')
        args = parser.parse_args()

        qry = Client.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        
        qry.client_key = args['client_key']
        qry.client_secret = args['client_secret']
        qry.status = args['status']
        db.session.commit()

        return marshal(qry, client_field), 200
    
    def delete(self, id):
        qry = Client.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        db.session.delete(qry)
        db.session.commit()
        
        return {'status': 'DELETED'}, 200

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

@app.errorhandler(exc.IntegrityError)
def handle_bad_request(e):
    return json.dumps({'status': 'BAD_REQUEST', 'message': str(e)}) \
        , 400 \
        , {'Content-Type': 'application/json'}

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=5000)