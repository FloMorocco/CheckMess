from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Spell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    effect = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    piece_compatibility = db.Column(db.String(80), nullable=False)
    target_type = db.Column(db.String(80), nullable=False)  # self, opponent, empty

class ActiveSpell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    spell_id = db.Column(db.Integer, db.ForeignKey('spell.id'), nullable=False)
    turns_left = db.Column(db.Integer, nullable=False)
    target_piece = db.Column(db.String(80), nullable=True)  # Optional

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_state = db.Column(db.String(200), nullable=False)
    active_spells = db.relationship('ActiveSpell', backref='game', lazy=True)
