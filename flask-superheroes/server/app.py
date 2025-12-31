from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import request, jsonify
from models import db, Hero, Power, HeroPower


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)


@app.get('/heroes')
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([h.to_dict(only=('id','name','super_name')) for h in heroes])

@app.get('/heroes/<int:id>')
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return {"error": "Hero not found"}, 404
    return hero.to_dict()

@app.get('/powers')
def get_powers():
    return jsonify([p.to_dict() for p in Power.query.all()])

@app.get('/powers/<int:id>')
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return {"error": "Power not found"}, 404
    return power.to_dict()


@app.patch('/powers/<int:id>')
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return {"error": "Power not found"}, 404

    try:
        power.description = request.json['description']
        db.session.commit()
        return power.to_dict()
    except Exception as e:
        return {"errors": [str(e)]}, 400


@app.post('/hero_powers')
def create_hero_power():
    try:
        hp = HeroPower(
            strength=request.json['strength'],
            hero_id=request.json['hero_id'],
            power_id=request.json['power_id']
        )
        db.session.add(hp)
        db.session.commit()
        return hp.to_dict(), 201
    except Exception as e:
        return {"errors": [str(e)]}, 400
