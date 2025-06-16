from flask import Blueprint, request, jsonify
from models import db, Hero, Power, HeroPower
from sqlalchemy.exc import IntegrityError

bp = Blueprint('api', __name__)

@bp.route('/heroes', methods=['GET'])
def get_heroes():
    return jsonify([hero.to_dict() for hero in Hero.query.all()])

@bp.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    return jsonify(hero.to_dict())

@bp.route('/powers', methods=['GET'])
def get_powers():
    return jsonify([power.to_dict() for power in Power.query.all()])

@bp.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify(power.to_dict())

@bp.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()
    try:
        power.description = data.get('description')
        db.session.commit()
        return jsonify(power.to_dict())
    except ValueError as ve:
        return jsonify({"errors": [str(ve)]}), 400

@bp.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    try:
        hp = HeroPower(
            strength=data['strength'],
            power_id=data['power_id'],
            hero_id=data['hero_id']
        )
        db.session.add(hp)
        db.session.commit()

        return jsonify({
            **hp.to_dict(),
            "hero": hp.hero.to_dict(),
            "power": hp.power.to_dict()
        }), 201
    except (ValueError, KeyError) as ve:
        return jsonify({"errors": [str(ve)]}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"errors": ["Invalid hero or power ID."]}), 400
