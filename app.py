import os
import sqlalchemy
from flask import Flask, jsonify, request
from models import db,User,Games,Matches
from flask_migrate import Migrate

  
app = Flask(__name__)

##Setting the place for the db to run
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/pedrolo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Initializing the db (after registering the Models)
db.init_app(app)
#migration engine
migrate = Migrate(app, db)





# add a match with a specific user 
@app.route("/match/<int:uid>/<int:gid>",methods=["POST"])
def add_specific_match(uid,gid):
    json = request.get_json()
    user = User.query.get(uid)
    game = Games.query.get(gid)
    if user is not None:
        match = Matches(
            wager = json["wager"],
            date= json["date"],
            user_one= user.id,
            game = game.id,
        )
        db.session.add(match)
        db.session.commit()
        return jsonify(match.to_dict())
    else:
        return jsonify({"message":"user not found"})
    



    
    
    
# get all matches 
@app.route("/match/",methods=["GET"])
def get_matches():
    matches = Matches.query.all()
    response=[]
    
    for ma in matches:
        match = ma.to_dict()
        response.append(match)
    return jsonify({"data":response})
    



# add a user 
@app.route("/user",methods=["POST"])
def add_user():
    users = request.get_json()
    user = User(
        full_name = users["full_name"],
        password =users["password"],
        console =users["console"],
    )
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict())



# get a specific user  
@app.route("/user/<int:id>",methods=["GET"]) 
def get_a_specific_user(id):
    if id>0:
        user = User.query.get(id)
        response=user.to_dict()
        return jsonify({"message":"200","data":response})
    response = jsonify({"error":400,"message":"no member found"})
    response.status_code = 400
    return response
 
 
 
 
# get all users     
@app.route("/user",methods=["GET"])
def get_users():
    users = User.query.all()
    response=[]
    
    for us in users:
        user = us.to_dict()
        response.append(user)
    return jsonify({"data":response})

# getting all the games 
@app.route('/game',methods=["GET"])
def gett_all_games():
    games = Games.query.all()
    response=[]
    for g in games:
        game = g.to_dict()
        response.append(game)
    
    return jsonify({"data":response})
        
# adding a game 
@app.route('/game',methods=["POST"])
def add_game():
    camilo = request.get_json()
    game = Games(
        name=camilo["name"],
        category=camilo["category"],
    )
    db.session.add(game)
    db.session.commit()  
    return jsonify(game.to_dict())

# getting a specific game

@app.route('/game/<int:id>',methods=["GET"])
def get_specific_game(id):
    if id>0:
        game = Games.query.get(id)
        response=game.to_dict()
        
        return jsonify({"message":"200","data":response})
        
    response = jsonify({"error":400,"message":"no member found"})
    response.status_code = 400
    return response

app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))