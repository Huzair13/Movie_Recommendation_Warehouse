
from flask import Flask, Blueprint, jsonify,session
from flask_cors import CORS
from flask import request, url_for, redirect, render_template

from flask_pymongo import pymongo

from simple_app.endpoints import project_api_routes

# con_string = "mongodb+srv://huzair13:huz2002@cluster0.7927yqz.mongodb.net/?retryWrites=true&w=majority"

# client = pymongo.MongoClient(con_string)
# db = client.get_database('MovieData')

# users=pymongo.collection.Collection(db,'user_ratings')


def create_app():
    web_app = Flask(__name__)  
    CORS(web_app)

    api_blueprint = Blueprint('api_blueprint', __name__)
    api_blueprint = project_api_routes(api_blueprint)
    
    web_app.secret_key = 'Huz@1234'
    web_app.register_blueprint(api_blueprint, url_prefix='/api')    

    return web_app


app = create_app()

@app.route('/')
def testing():
    return render_template("login.html")

@app.route('/login')
def login():
    return render_template('Login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    CORS(app)
    app.run(host='0.0.0.0',debug=True)
