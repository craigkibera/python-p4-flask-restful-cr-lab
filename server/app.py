#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return jsonify([plant.to_dict() for plant in plants])

    def post(self):
        data = request.get_json()
        try:
            new_plant = Plant(
               
                name=data['name'],
                image=data['image'],
                price=data['price'],
            )
            db.session.add(new_plant)
            db.session.commit()  
            db.session.refresh(new_plant)  
            return make_response(new_plant.to_dict(), 201)
        except Exception as e:
            db.session.rollback()
            return make_response({"error": str(e)}, 400)
    

class PlantByID(Resource):
    def get(self, plant_id):
        plant = Plant.query.get(plant_id)
        if plant is None:
            return make_response({"error": "Plant not found"}, 404)
        return make_response(plant.to_dict(), 200)
    
        

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:plant_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
