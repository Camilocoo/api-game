from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
#Example Model Item 
#It represents an Item in a list
#you can use any name, first letter in CAPS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), nullable=False, unique=False)
    password = db.Column(db.String(80),nullable=False, unique=False)
    console = db.Column(db.String(80),nullable=False, unique=False)
    matches = db.relationship("Matches",lazy=True)
    
    def __repr__(self):
        return 'User: %s' % self.name
  
    def to_dict(self):
        aux= []
        for match in self.matches:
            aux.append(match.to_dict())
            
            
        return { 
          "id": self.id, 
          "full_name": self.full_name, 
          "password": self.password,
          "console": self.console, 
          "matches": aux, 
        }
    
class Matches(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    wager= db.Column(db.Integer,nullable=False,unique=False)
    winner = db.Column(db.String(80),nullable=True,unique=True)
    date = db.Column(db.String,nullable=False,unique=False)
    user_one = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False,unique=False)
    user_two = db.Column(db.Integer,nullable=True,unique=False)
    game = db.Column(db.Integer,db.ForeignKey('games.id'),nullable=False,unique=False)
    user_one_stop =db.Column(db.Boolean,nullable=True,unique=False)
    user_two_stop = db.Column(db.Boolean,nullable=True,unique=False)
    user_one_aproval = db.Column(db.Boolean,nullable=True,unique=False)
    user_two_aproval =  db.Column(db.Boolean,nullable=True,unique=False)
    final_score =  db.Column(db.Integer,nullable=True,unique=False)
    
    def __repr__(self):
        return 'Matches: %s' % self.id
  
    def to_dict(self):
        
        game = Games.query.get(self.game)
        
        return { 
            "id": self.id, 
            "wager": self.wager, 
            "winner": self.winner,
            "date": self.date, 
            "user_one": self.user_one, 
            "user_two":self.user_two,         
            "game":game.camilo(),
            "user_one_stop":self.user_one_stop, 
            "user_two_stop":self.user_two_stop,
            "user_one_aproval":self.user_one_aproval, 
            "user_two_aproval":self.user_two_aproval, 
            "final_score":self.final_score,
        }

class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(80),nullable=False,unique=True)
    category = db.Column(db.String(80),nullable=False,unique=False)
    available_matches = db.relationship("Matches",lazy=True)
    
    
    def __repr__(self):
        return 'Game: %s' % self.name
  
    def to_dict(self):
        aux=[]
        for match in self.available_matches:
            aux.append(match.to_dict())
        return { 
          "id": self.id, 
          "name": self.name, 
          "category": self.category, 
          "available_matches":aux,
        }
    
    def camilo(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category
        }
 
    