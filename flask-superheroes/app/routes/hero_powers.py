from flask import Blueprint, jsonify, request, abort
from app import db
from app.models import HeroPower, Hero, Power

hero_powers_bp = Blueprint('hero_powers', __name__)

@hero_powers_bp.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['strength', 'power_id', 'hero_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'errors': [f'{field} is required']}), 400
    
    # Validate strength
    valid_strengths = ['Strong', 'Weak', 'Average']
    if data['strength'] not in valid_strengths:
        return jsonify({'errors': [f'strength must be one of: {", ".join(valid_strengths)}']}), 400
    
    # Check if hero exists
    hero = Hero.query.get(data['hero_id'])
    if not hero:
        return jsonify({'errors': ['Hero not found']}), 404
    
    # Check if power exists
    power = Power.query.get(data['power_id'])
    if not power:
        return jsonify({'errors': ['Power not found']}), 404
    
    # Check if relationship already exists
    existing = HeroPower.query.filter_by(
        hero_id=data['hero_id'],
        power_id=data['power_id']
    ).first()
    
    if existing:
        return jsonify({'errors': ['This hero already has this power']}), 400
    
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
        return jsonify({'errors': [str(e)]}), 400