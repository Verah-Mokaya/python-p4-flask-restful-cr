#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    pass

class Newsletters(Resource):

    def get(self):
        response_dict_list = [newsletter.to_dict() for newsletter in Newsletter.query.all()]
        response = make_response(response_dict_list, 200)
        return response

    def post(self):
        data = request.get_json()
        new_newsletter = Newsletter(
            title=data.get('title'),
            description=data.get('description'),
            frequency=data.get('frequency')
        )
        db.session.add(new_newsletter)
        db.session.commit()
        response = make_response(new_newsletter.to_dict(), 201)
        return response
    
api.add_resource(Newsletters, '/newsletters')

class NewletterByID(Resource):

    def get(self, id):
        newsletter = Newsletter.query.get(id)
        if newsletter:
            response = make_response(newsletter.to_dict(), 200)
        else:
            response = make_response({'error': 'Newsletter not found'}, 404)
        return response

api.add_resource(NewletterByID, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
