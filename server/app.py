#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


@app.route('/plants', methods=['GET', 'POST'])
def all_plants():
    if request.method == 'GET':
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)
    elif request.method == 'POST':
        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)


@app.route('/plants/<int:id>', methods=['GET'])
def plant_by_id(id):
    if request.method == 'GET':
        plant = Plant.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(plant), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
