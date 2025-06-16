from flask import Blueprint, request, jsonify
from models import db, Hero, Power, HeroPower

api = Blueprint('api', __name__)

# 1. GET /heroes - List all heroes
@api.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_list = [
        {"id": hero.id, "name": hero.name, "super_name": hero.super_name}
        for hero in heroes
    ]
    return jsonify(hero_list), 200

# 2. GET /heroes/<id> - Get a single hero by ID, including powers
@api.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404

    hero_data = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "powers": [
            {
                "id": hp.power.id,
                "name": hp.power.name,
                "description": hp.power.description
            }
            for hp in hero.hero_powers
        ]
    }
    return jsonify(hero_data), 200

# 3. GET /powers - List all powers
@api.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_list = [
        {"id": power.id, "name": power.name, "description": power.description}
        for power in powers
    ]
    return jsonify(power_list), 200

# 4. GET /powers/<id> - Get a single power by ID
@api.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify(power.to_dict()), 200

# 5. PATCH /powers/<id> - Update power description (with validation)
@api.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()
    description = data.get("description", "").strip()

    if not description or len(description) < 20:
        return jsonify({"errors": ["Description must be at least 20 characters long"]}), 400

    power.description = description
    db.session.commit()

    return jsonify(power.to_dict()), 200

# 6. POST /hero_powers - Create a HeroPower association
@api.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()

    strength = data.get('strength')
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')

    # Validate strength value
    if strength not in ['Strong', 'Weak', 'Average']:
        return jsonify({"errors": ["Strength must be 'Strong', 'Weak', or 'Average'"]}), 400

    # Validate hero and power existence
    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)
    if not hero or not power:
        return jsonify({"errors": ["Invalid hero_id or power_id"]}), 400

    new_hero_power = HeroPower(
        strength=strength,
        hero_id=hero_id,
        power_id=power_id
    )

    db.session.add(new_hero_power)
    db.session.commit()

    # Return updated hero with powers
    updated_hero = Hero.query.get(hero_id)
    hero_data = {
        "id": updated_hero.id,
        "name": updated_hero.name,
        "super_name": updated_hero.super_name,
        "powers": [
            {
                "id": hp.power.id,
                "name": hp.power.name,
                "description": hp.power.description
            }
            for hp in updated_hero.hero_powers
        ]
    }

    return jsonify(hero_data), 201

# 7. DELETE /heroes/<id> - Delete a hero by ID
@api.route('/heroes/<int:id>', methods=['DELETE'])
def delete_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404

    db.session.delete(hero)
    db.session.commit()

    return '', 204

# Optional: Root route for API welcome message
@api.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to the Superheroes API!"})
