from flask import Blueprint, jsonify
from app import db
from app.models import Hero

#url_prefix
heroes_bp = Blueprint('heroes', __name__, url_prefix='/')

@heroes_bp.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes])

@heroes_bp.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404
    
    return jsonify(hero.to_dict_with_powers())