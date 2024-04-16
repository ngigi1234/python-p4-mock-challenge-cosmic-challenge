#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)


@app.route('/')
def home():
    return ''

class Scientists_Route(Resource):

    def get(self):
        try:
            scientists = [scientist.to_dict(only=("id", "name", "field_of_study")) for scientist in Scientist.query.all()]
            return scientists, 200
        except:
            return {"error": "Bad request"}, 400

    
    def post(self):
        try:
            data = request.get_json()
            new_scientist = Scientist(
                name = data['name'],
                field_of_study = data['field_of_study']
            )
            db.session.add(new_scientist)
            db.session.commit()

            return new_scientist.to_dict(only=("id", "name", "field_of_study", "missions")), 201
        except Exception as e:
            print(e)
            return { "errors": ["validation errors"] }, 400



class ScientistByID_Route(Resource):
        
    def get(self, id):
            scientist = Scientist.query.filter(Scientist.id == id).first()
            if scientist:
                return scientist.to_dict(), 200
            else: 
                return {"error": "Scientist not found"}, 404
        
    def patch(self, id):
        scientist = Scientist.query.filter(Scientist.id==id).first()
        if scientist:
            try:
                data = request.get_json()
                for attr in data:
                    setattr(scientist, attr, data[attr])
                db.session.add(scientist)
                db.session.commit()
                return scientist.to_dict(), 202
            except Exception as e: #e will save the actual error cause
                print(e)           #print(e) so you can see the error cause
                return {"errors": ["validation errors"]}, 400
        else:
            return {"error": "Scientist not found"}, 404
        
    def delete(self, id):
        scientist = Scientist.query.filter(Scientist.id == id).first()
        # print(scientist)
        if scientist:
            allMissions = Mission.query.filter(Mission.scientist_id == id).all()
            for mission in allMissions:
                db.session.delete(mission)
            db.session.delete(scientist)
            db.session.commit()
            return {}, 204
        else:
            return {"error": "Scientist not found"}, 404



class Planets_Route(Resource):

    def get(self):
        try:
            planets = [planet.to_dict(only=("id", "name", "distance_from_earth", "nearest_star")) for planet in Planet.query.all()]
            return planets, 200
        except:
            return {"error": "Bad request"}, 400



class Missions_Route(Resource):
    
    def post(self):
        try:
            data = request.get_json()
            new_mission = Mission(
                name = data['name'],
                scientist_id = data['scientist_id'],
                planet_id = data['planet_id']
            )
            db.session.add(new_mission)
            db.session.commit()

            return new_mission.to_dict(), 201
        except Exception as e:
            print(e)
            return { "errors": ["validation errors"] }, 400


api.add_resource(Scientists_Route, '/scientists')
api.add_resource(ScientistByID_Route, '/scientists/<int:id>')
api.add_resource(Planets_Route, '/planets')
api.add_resource(Missions_Route, '/missions')




if __name__ == '__main__':
    app.run(port=5555, debug=True)


# 1 check is if-else
# multi-check is try-except