# server/app.py

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

# --- API ROUTES ---

@app.route('/games')
def games():
    # Use list comprehension to serialize all game records
    games = [game.to_dict() for game in Game.query.all()]
    
    return make_response(
        games,
        200
    )

@app.route('/games/<int:id>')
def game_by_id(id):
    # Find a specific game by ID
    game = Game.query.filter(Game.id == id).first()
    
    if not game:
        return make_response({"error": "Game not found"}, 404)

    # Convert the single game object to a dictionary
    game_dict = game.to_dict()

    return make_response(
        game_dict,
        200
    )

@app.route('/games/users/<int:id>')
def game_users_by_id(id):
    # Find the game first
    game = Game.query.filter(Game.id == id).first()
    
    if not game:
        return make_response({"error": "Game not found"}, 404)

    # Use association proxy to get users for a game
    # We pass a rule to avoid sending the user's reviews list again (prevents clutter)
    users = [user.to_dict(rules=("-reviews",)) for user in game.users]
    
    return make_response(
        users,
        200
    )

if __name__ == '__main__':
    app.run(port=5555, debug=True)