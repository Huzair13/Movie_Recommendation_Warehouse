import logging

from flask_pymongo import pymongo
from flask import jsonify, request,session,make_response
from flask import  url_for, redirect, render_template
from pandas.tseries.offsets import DateOffset
import pandas as pd
from scipy import sparse

import pandas as pd
import bcrypt
import json
from statsmodels.tsa.stattools import adfuller
from pandas.tseries.offsets import DateOffset
import io
import matplotlib.dates as mdates
import base64
import statsmodels.api as sm

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import requests

api_endpoint = 'https://api.themoviedb.org/3/find/'
api_key = '8134811032100258ec27af24089d17a1'


import pickle

con_string = "mongodb+srv://huzair13:huz2002@cluster0.7927yqz.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_string)

db = client.get_database('MovieData')



user_collection = pymongo.collection.Collection(db, 'movies') #(<database_name>,"<collection_name>")

movies=pymongo.collection.Collection(db,'movies')
users=pymongo.collection.Collection(db,'user_ratings')


print("MongoDB connected Successfully")

# with open('finalized_model.pkl', 'rb') as f:
#     model, params = pickle.load(f)



def project_api_routes(endpoints):


    @endpoints.after_request
    def add_header(response):
        response.cache_control.no_cache = True
        response.cache_control.no_store = True
        response.cache_control.must_revalidate = True
        response.cache_control.max_age = 0
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response


    @endpoints.route("/")
    def index():
        return render_template("testing.html")

    @endpoints.route('/hello', methods=['GET'])
    def hello():
        res = 'Hello world heyyyyyyyyyyyy'
        print("Hello world Hellow")
        print(res)
        return res

    @endpoints.route('/register- user', methods=['POST'])
    def register_user():
        resp = {}
        try:
            req_body = request.json
            # resp['hello'] = hello_world
            # req_body = req_body.to_dict()
            user_collection.insert_one(req_body)            
            print("User Data Stored Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Stored Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp


    @endpoints.route('/register-user2', methods=['POST'])
    def register_user_new2():
        resp = {}
        try:
            req_body = request.json
            # resp['hello'] = hello_world
            # req_body = req_body.to_dict()
            users.insert_one(req_body)            
            print("User Data Stored Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Stored Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp

    

    
    @endpoints.route('/register-user1', methods=['POST'])
    def register_user_new():
        resp = {}
        try:
            data = request.json
            # resp['hello'] = hello_world
            # req_body = req_body.to_dict()
            result = user_collection.find_one({'id': data['id'], 'name': data['name'], 'email': data['email']})

            if result:
                print("Data Already Exists")
                status = {
                    "statusCode":"400",
                    "statusMessage":"User Data Stored NOT Successfully in the Database."
                }
            else:
                user_collection.insert_one(data)
                print("User Data Stored Successfully in the Database.")
                status = {
                    "statusCode":"200",
                    "statusMessage":"User Data Stored Successfully in the Database."
                }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp




    @endpoints.route('/update-users',methods=['POST'])
    def update_users():
        resp = {}
        try:
            name = request.json['name']
            mid=request.json['id']
            rating =request.json['rating']
            users.update_one({"name":name}, {"$set": {mid : str(rating)}},upsert=True)
            print("User Data Updated Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Updated Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp    

    @endpoints.route('/update_rat',methods=['PUT'])
    def update_rat():
        resp = {}
        try:
            req_body = request.json
            # Search for the user with the specified username and insert the id and rating in the user document
            users.update_one({"name": req_body["name"]}, {"$set": {req_body["id"] : req_body["rating"]}},upsert=True)
            print("User Data Updated Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Updated Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] = status
        return resp     


    @endpoints.route('/delete',methods=['DELETE'])
    def delete():
        resp = {}
        try:
            delete_id = request.args.get('delete_id')
            user_collection.delete_one({"name":delete_id})
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Deleted Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp
    
    

    #USER SIGNIN AND SIGNUP

    @endpoints.route('/signup', methods=['POST'])
    def signup():
        try:
            username = request.json['name']
            email=request.json['email']
            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(request.json['password'].encode('utf-8'), salt)
            user = {'name': username, 'password': password,'email':email}

            if users.find_one({'name': username}) or users.find_one({'email':email}):
                status = {
                "statusCode":"400",
                "statusMessage":"Username or email alread exists"
                }

            else :
                users.insert_one(user)
                print("User Data Stored Successfully in the Database.")
                status = {
                    "statusCode":"200",
                    "statusMessage":"User Data Stored Successfully in the Database."
                    }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }

        return jsonify(status)

    @endpoints.route('/signin', methods=['POST'])
    def signin():
        username = request.json['name']
        password = request.json['password']

        user = users.find_one({'name': username})

        if user and bcrypt.hashpw(password.encode('utf-8'), user['password']) == user['password']:
            session['user'] = username
            response = {'statusCode': 200, 'statusMessage': 'User logged in successfully'}
        else:
            response = {'statusCode': 400, 'statusMessage': 'Invalid credentials'}
    
        return jsonify(response)



    @endpoints.route('/logout',methods=['DELETE'])
    def logout():
        session.pop('user', None)
        return jsonify({'statusCode': 200, 'statusMessage': 'User logged out successfully'})


    
    @endpoints.route('/download_prediction',methods=['POST','GET'])
    def download():

        json_data = request.get_json()
        df = pd.DataFrame(json_data)
        csv_string = df.to_csv(index=False)
        response = make_response(csv_string)
        response.headers.set('Content-Disposition', 'attachment', filename='data.csv')
        response.headers.set('Content-Type', 'text/csv')

        return response
    
    @endpoints.route('/read-data',methods=['GET'])
    def read_data():
        resp = {}
        try:
            movie_id = request.args.get('id')
            users_list = movies.find({"id": movie_id})
            users_list = list(users_list)
            status = {
                "statusCode":"200",
                "statusMessage":"Data Retrieval Successfull"
            }
            output = [{'adult' : user['adult'], 'budget' : user['budget'],'genres' : user['genres'],
            'id' : user['id'],'imdb_id' : user['imdb_id'],'original_language' : user['original_language'],'original_title' : user['original_title'],
            'overview' : user['overview'],'popularity' : user['popularity'],'poster_path' : user['poster_path'],'release_date' : user['release_date'],
            'revenue' : user['revenue'],'status' : user['status'],'vote_average' : user['vote_average'],'vote_count' : user['vote_count'],
            'cast' : user['cast'],'crew' : user['crew']} for user in users_list]  

            resp['data'] = output
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        print(resp)
        return resp

    @endpoints.route('/getdata',methods=['POST'])
    def getmoviedata():
        resp = {}
        movies_list = []  # Create an empty list to store the movie objects
        response = request.get_json()

        try:
            for key in response:
                print(key)
                r=read_m(key)
                if (r!=[]):
                    movies_list.append(read_m(key))
            status = {
                "statusCode": "200",
                "statusMessage": "Success"
            }

        except Exception as e:
            print(e)
            status = {
                "statusCode": "400",
                "statusMessage": str(e)
            }

        # movies_list=df.to_dict(orient='records')

        resp["status"] = status
        resp["movies"] = movies_list  # Add the movies list to the response dictionary
        return resp

    def read_m(movie_id):
        resp = {}
        try:
            users_list = movies.find({"id": movie_id})
            users_list = list(users_list)
            status = {
                "statusCode":"200",
                "statusMessage":"Data Retrieval Successfull"
            }
            output = [{'genres' : user['genres'],
            'id' : user['id'],'imdb_id' : user['imdb_id'],'original_language' : user['original_language'],'original_title' : user['original_title'],
            'overview' : user['overview'],'popularity' : user['popularity'],'poster_path' : user['poster_path'],'release_date' : user['release_date'],
            'vote_average' : user['vote_average'],'vote_count' : user['vote_count'],
            'cast' : user['cast'],'crew' : user['crew']} for user in users_list]

            print(output) 
            resp['data'] = output
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }

        resp["status"] =status
        print(resp)
        return output

    @endpoints.route('/random',methods=['POST'])
    def hellonew():
        resp={}
        try:
            username =request.json['username']
            document = movies.aggregate([{ "$sample": { "size": 10 } }])
            result = {}
            for doc in document:
                result[str(doc['id'])] = float(doc['vote_average'])//2

            resp["data"]=result

            status={
                "statusCode":"200",
                "statusMessage":"success"
            }

            resp["status"] =status
            print(result)
            return resp
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
            resp['status']=status
            return resp

    @endpoints.route('/pred_rat',methods=['post'])
    def pred_rat():
        resp = {}
        try:
            # username = request.args.get('username')
            username =request.json['username']
            print(username)

            document = users.find_one({"name": username})
            keys_to_remove = {"_id","name", "email","password"}
            result = [(key, float(value)) for key, value in document.items() if key not in keys_to_remove]
            print(result)

            rating=pd.read_csv('ratings_small.csv')
            rating.rename(columns={'movieId': 'id'}, inplace=True)
            rating['id']=rating['id'].astype(str)
            userRatings = rating.pivot_table(index=['userId'],columns=['id'],values='rating')
            userRatings.head()
            userRatings = userRatings.dropna(thresh=10, axis=1).fillna(0,axis=1)
            corrMatrix = userRatings.corr(method='pearson')
            # data = [("1007",5),("100",3),("1009",1),("110102",2)]
            print(result)

            rated_movies = result
            rated_df = pd.DataFrame(rated_movies, columns=['id', 'rating'])
            rated_df = rated_df.set_index('id')
            similar_movies = pd.DataFrame()
            for movie,rating in rated_movies:
                similar_movies = similar_movies.append(get_similar(movie,rating,corrMatrix),ignore_index = True)

            similar_movies = similar_movies.sum().sort_values(ascending=False)
            print(similar_movies)
            print("------------------------------------")
            similar_movies = similar_movies.loc[~(similar_movies.index).isin(rated_df.index)]
            print(similar_movies)

            similar_movies =similar_movies.head(30)

            similar_movies_dict = similar_movies.to_dict()
            similar_movies_json = json.dumps(similar_movies_dict)
            similar = json.loads(similar_movies_json)
            print(similar)

            resp["data"]=similar

            status={
                "statusCode":"200",
                "statusMessage":"success"
            }
            if(resp["data"]=={}):
                status={
                    "statusCode":"200",
                    "statusMessage":"novalue"
                }
            print(status)
            resp["status"] =status
            print(resp)
            print("hidszkjasdaf")
            return resp

        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
            resp["status"] =status
            return resp
        
    def get_similar(movie_name,rating,corrMatrix):
        similar_ratings = corrMatrix[movie_name]*(rating-2.5)
        similar_ratings = similar_ratings.sort_values(ascending=False)
        return similar_ratings

    def get_poster_path(imdb_id):
        url = f'{api_endpoint}{imdb_id}?api_key={api_key}&external_source=imdb_id'
        response = requests.get(url).json()
        poster_path = response['movie_results'][0]['poster_path']
        return poster_path

    return endpoints