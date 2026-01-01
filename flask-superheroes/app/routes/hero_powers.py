from flask import Blueprint, jsonify, request
from app import db
from app.models import HeroPower, Hero, Power

# url_prefix
hero_powers_bp = Blueprint('hero_powers', __name__, url_prefix='/')

@hero_powers_bp.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    
    if not data:
        return jsonify({'errors': ['No data provided']}), 400
    
    required_fields = ['strength', 'power_id', 'hero_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'errors': [f'{field} is required']}), 400
    
    valid_strengths = ['Strong', 'Weak', 'Average']
    if data['strength'] not in valid_strengths:
        return jsonify({'errors': [f'strength must be one of: {", ".join(valid_strengths)}']}), 400
    
    hero = Hero.query.get(data['hero_id'])
    if not hero:
        return jsonify({'errors': ['Hero not found']}), 404
    
    power = Power.query.get(data['power_id'])
    if not power:
        return jsonify({'errors': ['Power not found']}), 404
    
    try:
        hero_power = HeroPower(
            strength=data['strength'],
            hero_id=data['hero_id'],
            power_id=data['power_id']
        )
        
        db.session.add(hero_power)
        db.session.commit()
        
        return jsonify(hero_power.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': ['Validation error']}), 400