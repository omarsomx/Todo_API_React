"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Todo
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Todo.get_all()

    lista_todo = []
    for task in tasks:
        lista_todo.append(task.serialize())

    return jsonify(lista_todo), 200

@app.route('/task/<int:id>', methods=['GET'])
def get_id(id):
    
    task = Todo.get_id(id)

    if task:
        return jsonify(task.serialize()), 200
    else:
        return jsonify({"message" :f'The task {id} does not exist.'}), 401

@app.route('/create_task', methods=['POST'])
def create_task():
    req_body = request.get_json()
    title = req_body["title"]
    
    if title:
        try:
            task = Todo.create_task(title)
            return jsonify({"message" :" Successfully registered.","task":task.serialize()}), 201
            
        except Exception as e:
            print("Create proccess has failed", e)
            raise APIException("Create process has failed", 401)
    else:
        return jsonify({"message" :"The task does not have title."}), 401
    

@app.route('/task/update/<int:id>', methods=['POST'])
def update_task(id):
    req_body = request.get_json()
    title = req_body["title"]
    
    task = Todo.get_id(id)

    if task:
        try:
            update_task = task.update_task(title)

            return jsonify({"message" :" Successfully updated.","task":task.serialize()}), 201

        except Exception as e:
            print("Update proccess has failed", e)
            raise APIException("Update process has failed", 401)
    else:
        return jsonify({"message" :"The task does not exist."}), 401

@app.route('/task/delete/<int:id>', methods=['DELETE'])
def delete_todo(id):
    task = Todo.get_id(id)

    if task:
        try:
            destroy_task = task.destroy()

            return "Todo " + str(id) + " was successfully deleted", 200

        except Exception as e:
            print("Ppdate proccess has failed", e)
            raise APIException("Update process has failed", 401)
    else:
        return jsonify({"message" :f'The task {id} does not exist.'}), 400

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
