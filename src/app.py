"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# get all family members
@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()

    if not members: return jsonify({'status': 'failed','message': 'Something went wrong'}), 400

    return jsonify(members), 200

# Add a new family member
@app.route('/member', methods=['POST'])
def add_member():
    first_name = request.json.get('first_name')
    lucky_numbers = request.json.get('lucky_numbers')
    age = request.json.get('age')

    if not first_name: return jsonify({'message': 'First Name is required'}), 400
    if not lucky_numbers: jsonify({'message': 'Age is required'}), 400
    if not age: return jsonify({'message': 'Lucky Numbers is required'}), 400

    new_member = {
        'id': request.json.get('id') if request.json.get('id') is not None else jackson_family._generateId(),
        'first_name': first_name,
        'last_name': jackson_family.last_name,
        'age': age,
        'lucky_numbers': lucky_numbers
    }

    response = jackson_family.add_member(new_member)

    return jsonify({'status': 'success', 'message': response})

# Get a family member by id
@app.route('/member/<int:member_id>', methods=['GET'])
def get_family_member(member_id):
    member = jackson_family.get_member(member_id)

    if member:
        return jsonify(member), 200
    else: 
        return jsonify({'status': 'failed', 'message': 'Member not found'}), 400


# Delete a family member by id
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_family_member(member_id):
    member = jackson_family.get_member(member_id)

    if member:
        jackson_family.delete_member(member_id)
        return jsonify({'status': 'success', 'message': 'Member deleted'}), 200
    else: 
        return jsonify({'status': 'failed', 'message': 'Member not found'}), 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
